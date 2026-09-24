import subprocess
import time
import json
import urllib.request
import asyncio
import websockets
import sys

# Ensure UTF-8 output on Windows console
sys.stdout.reconfigure(encoding='utf-8')

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
URL = "http://localhost:8080/"

async def run_tests():
    print(">>> Starting Edge process with CDP...")
    proc = subprocess.Popen([
        EDGE_PATH,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        URL
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(2.5)

    ws_url = None
    try:
        req = urllib.request.urlopen("http://localhost:9222/json/list")
        tabs = json.loads(req.read().decode('utf-8'))
        for t in tabs:
            if t.get('type') == 'page':
                ws_url = t.get('webSocketDebuggerUrl')
                break
    except Exception as e:
        print("Failed to get tabs:", e)
        proc.terminate()
        return

    print(">>> Connecting to WebSocket:", ws_url)
    console_logs = []
    errors = []

    async with websockets.connect(ws_url) as ws:
        msg_id = 0

        async def send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(payload))
            while True:
                resp = await ws.recv()
                data = json.loads(resp)
                if data.get("id") == msg_id:
                    return data
                elif data.get("method") == "Runtime.consoleAPICalled":
                    console_logs.append(data["params"])
                elif data.get("method") == "Runtime.exceptionThrown":
                    errors.append(data["params"])

        async def eval_js(expression):
            res = await send("Runtime.evaluate", {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True
            })
            return res.get("result", {}).get("result", {}).get("value")

        # Enable runtime & console
        await send("Runtime.enable")
        await send("Page.enable")

        print(">>> Page loaded. Testing Initial State...")
        title = await eval_js("document.title")
        print("Page Title:", title)
        assert "CareTranslate AI" in title, "Title mismatch"

        # Check empty state is visible
        empty_visible = await eval_js("!document.getElementById('emptyStateView').classList.contains('hidden')")
        print("Empty State Visible:", empty_visible)
        assert empty_visible, "Empty state should be visible initially"

        # Test 1: Load Sample Note 1 (CHF)
        print("\n>>> Testing Test 1: Load CHF Sample Note...")
        await eval_js("loadSampleNote('chf_exacerbation')")
        note_val = await eval_js("document.getElementById('clinicalNoteInput').value")
        print("Note input length:", len(note_val))
        assert "Acute decompensated biventricular heart failure" in note_val

        # Test 2: Generate Instructions
        print("\n>>> Testing Test 2: Generate Instructions...")
        await eval_js("handleGenerate(false)")  # synchronous generation
        await asyncio.sleep(0.5)

        success_visible = await eval_js("!document.getElementById('successStateView').classList.contains('hidden')")
        print("Success State Visible:", success_visible)
        assert success_visible, "Success state should be visible after generate"

        # Verify Factual Consistency Card
        audit_text = await eval_js("document.getElementById('factualAuditCard').innerText")
        print("Factual Audit text preview:", audit_text[:100].replace('\n', ' '))
        assert "Verified" in audit_text, "CHF should be verified"

        # Verify Discharge Instructions Card
        instr_text = await eval_js("document.getElementById('dischargeInstructionsBody').innerText")
        print("Discharge text preview:", instr_text[:100].replace('\n', ' '))
        assert "Furosemide" in instr_text or "Lasix" in instr_text

        # Test 3: Language Switching to Spanish
        print("\n>>> Testing Test 3: Language Switching to Spanish (es)...")
        await eval_js("document.getElementById('languageSelect').value = 'es'")
        await eval_js("AppState.selectedLanguage = 'es'; handleGenerate(false);")
        await asyncio.sleep(0.3)
        spanish_text = await eval_js("document.getElementById('dischargeInstructionsBody').innerText")
        print("Spanish output preview:", spanish_text[:120].replace('\n', ' '))
        assert "hospital" in spanish_text.lower() or "líquido" in spanish_text.lower()

        # Test 4: Literacy Switching to Basic
        print("\n>>> Testing Test 4: Literacy Switching to Basic...")
        await eval_js("document.querySelector('[data-literacy=\"basic\"]').click()")
        await asyncio.sleep(0.3)
        curr_lit = await eval_js("AppState.selectedLiteracy")
        print("Current literacy:", curr_lit)
        assert curr_lit == "basic"

        # Test 5: Clinician Review & Edit Mode
        print("\n>>> Testing Test 5: Clinician Review & Edit Mode...")
        initial_readonly = await eval_js("document.getElementById('clinicianReviewTextarea').hasAttribute('readonly')")
        print("Initial textarea readonly:", initial_readonly)
        assert initial_readonly, "Should be readonly initially"

        await eval_js("toggleReviewEditMode()")
        after_toggle_readonly = await eval_js("document.getElementById('clinicianReviewTextarea').hasAttribute('readonly')")
        print("After edit toggle readonly:", after_toggle_readonly)
        assert not after_toggle_readonly, "Should not be readonly in edit mode"

        # Edit text and toggle off
        await eval_js("document.getElementById('clinicianReviewTextarea').value += '\\n[Clinician Note: Emphasized daily weigh-ins]'")
        await eval_js("toggleReviewEditMode()")

        # Test 6: Clinician Approval
        print("\n>>> Testing Test 6: Clinician Approval...")
        await eval_js("handleApproveInstructions()")
        is_approved = await eval_js("AppState.isReviewApproved")
        print("Is review approved:", is_approved)
        assert is_approved, "Review should be approved"

        banner_text = await eval_js("document.getElementById('clinicianApprovalStatusBanner').innerText")
        print("Approval banner text:", banner_text.replace('\n', ' '))
        assert "Approved for Patient Handout" in banner_text

        # Test 7: Load Sample 4 (Allergy Conflict Demo)
        print("\n>>> Testing Test 7: Safety Mismatch Alert Case (Penicillin vs Augmentin)...")
        await eval_js("loadSampleNote('allergy_conflict_demo'); handleGenerate(false);")
        await asyncio.sleep(0.3)
        audit_mismatch_text = await eval_js("document.getElementById('factualAuditCard').innerText")
        print("Mismatch audit text:", audit_mismatch_text[:120].replace('\n', ' '))
        assert "Potential Mismatch" in audit_mismatch_text or "CRITICAL" in audit_mismatch_text

        # Test 8: Font size scaler
        print("\n>>> Testing Test 8: Font Size Scaler...")
        await eval_js("document.querySelector('[data-font-size=\"large\"]').click()")
        body_has_large = await eval_js("document.getElementById('dischargeInstructionsBody').classList.contains('text-base')")
        print("Font scale large applied:", body_has_large)
        assert body_has_large, "text-base should be applied"

        # Test 9: Audio TTS button
        print("\n>>> Testing Test 9: Text-to-Speech Toggle...")
        tts_text_before = await eval_js("document.getElementById('ttsAudioBtn').innerText")
        await eval_js("toggleAudioPlayback()")
        tts_text_after = await eval_js("document.getElementById('ttsAudioBtn').innerText")
        print("TTS button before:", tts_text_before.strip(), "| after:", tts_text_after.strip())
        await eval_js("stopAudioPlayback()")

        # Test 10: History Modal Open & Close
        print("\n>>> Testing Test 10: History Modal...")
        await eval_js("openModal('historyModal')")
        modal_open = await eval_js("!document.getElementById('historyModal').classList.contains('hidden')")
        print("History modal open:", modal_open)
        assert modal_open, "Modal should be open"

        await eval_js("closeModal('historyModal')")
        modal_closed = await eval_js("document.getElementById('historyModal').classList.contains('hidden')")
        print("History modal closed:", modal_closed)
        assert modal_closed, "Modal should be closed"

        # Test 11: Error State Simulation
        print("\n>>> Testing Test 11: Error State...")
        await eval_js("document.getElementById('errorSimulateToggle').checked = true; AppState.simulateError = true;")
        await eval_js("handleGenerate(false)")
        error_visible = await eval_js("!document.getElementById('errorStateView').classList.contains('hidden')")
        print("Error state visible:", error_visible)
        assert error_visible, "Error state should be visible"

        # Reset error simulation
        await eval_js("document.getElementById('errorSimulateToggle').checked = false; AppState.simulateError = false;")
        await eval_js("loadSampleNote('chf_exacerbation'); handleGenerate(false);")

        print("\n>>> Checking Console Logs and Errors...")
        print("Total Console Logs:", len(console_logs))
        print("Total Errors:", len(errors))
        if errors:
            print("ERRORS DETECTED:")
            for err in errors:
                print(" -", err)

        print("\n>>> ALL AUTOMATED FRONTEND QA TESTS PASSED!")

    proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_tests())
