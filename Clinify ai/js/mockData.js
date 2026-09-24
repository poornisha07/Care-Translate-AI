/**
 * CareTranslate AI - Mock Clinical Data & Translation Presets
 * Designed for hackathon demonstration with authentic medical vocabulary and safety rules.
 */

const MOCK_DATA = {
  // Current user info
  currentUser: {
    name: "Dr. Sarah Lin, MD",
    role: "Attending Physician",
    department: "Acute Internal Medicine",
    facility: "Metropolitan General Hospital",
    avatar: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=200",
    badge: "Staff Clinician"
  },

  // Sample Clinical Notes
  samples: [
    {
      id: "chf_exacerbation",
      title: "CHF Exacerbation & Diuretic Optimization",
      category: "Cardiology",
      tag: "Verified",
      patientInfo: {
        name: "Robert Hernandez",
        age: 68,
        mrn: "MRN-849201",
        admissionDate: "2026-09-21",
        dischargeDate: "2026-09-24",
        attending: "Dr. Sarah Lin, MD"
      },
      originalNote: `HOSPITAL DISCHARGE SUMMARY
PATIENT: Hernandez, Robert | MRN: 849201 | AGE: 68 | SEX: M
ADMISSION DATE: 09/21/2026 | DISCHARGE DATE: 09/24/2026
ATTENDING: Sarah Lin, MD | SERVICE: Internal Medicine

DIAGNOSIS:
1. Acute decompensated biventricular heart failure (HFrEF, EF 32%), resolved with IV loop diuretic therapy.
2. Chronic essential hypertension.
3. Mild hyperkalemia (resolved, K+ 4.3 mEq/L at discharge).

HOSPITAL COURSE & REASON FOR ADMISSION:
Patient presented via ED with progressive dyspnea on exertion (NYHA Class III/IV), orthopnea requiring 3 pillows, and bilateral lower extremity pitting edema (+3). Successfully diuresed with IV Furosemide (80mg BID x 48h) with net negative fluid balance of 4.2 Liters. Weight decreased from 89.4 kg to 85.2 kg. Renal function stable (Creatinine 1.05 mg/dL).

DISCHARGE MEDICATIONS:
1. Furosemide (Lasix) 40 mg PO daily each morning at 08:00. (DO NOT take in evening to prevent nocturia).
2. Lisinopril 10 mg PO once daily.
3. Carvedilol 6.25 mg PO BID with meals (08:00, 18:00).
4. Potassium Chloride (Klor-Con) 20 mEq PO daily with morning meal.

DISCHARGE ORDERS & PRECAUTIONS:
- Strict sodium restriction: < 2,000 mg Na+ per day.
- Daily fluid restriction: Maximum 1,500 mL (approx. 50 oz) total fluids daily.
- Daily weight monitoring: Patient must weigh self every morning post-voiding, prior to breakfast, on same scale.
- Call clinic immediately if weight increases > 3 lbs in 24 hours or > 5 lbs in 7 days.
- Red flag symptoms: Paroxysmal nocturnal dyspnea, increased lower extremity edema, persistent dry cough, chest pain, lightheadedness.

FOLLOW-UP APPOINTMENTS:
- Heart Failure Clinic with Dr. Lin in 7 days (09/30/2026 at 10:30 AM).
- BMP (Basic Metabolic Panel) to check electrolytes and renal panel in 5 days at Outpatient Lab.`,
      
      // Generated translations by Literacy & Language
      translations: {
        "en": {
          "basic": {
            overview: "You came to the hospital because your heart was having trouble pumping extra fluid out of your body, which made it hard to breathe and caused swelling in your legs. We gave you medicine to drain the fluid, and you are now safe to rest and heal at home.",
            medications: [
              {
                name: "Furosemide (Lasix) - 40 mg",
                nickname: "Water pill",
                timing: "Take 1 pill every morning at 8:00 AM with water",
                purpose: "Helps your body pee out extra water so fluid doesn't build up in your lungs.",
                warning: "Take this in the morning so you don't have to wake up at night to use the bathroom."
              },
              {
                name: "Carvedilol - 6.25 mg",
                nickname: "Heart protector pill",
                timing: "Take 1 pill two times a day (breakfast and dinner)",
                purpose: "Helps your heart beat gently and keeps your blood pressure healthy.",
                warning: "Take with food to prevent feeling dizzy."
              },
              {
                name: "Lisinopril - 10 mg",
                nickname: "Blood pressure pill",
                timing: "Take 1 pill every day in the morning",
                purpose: "Relaxes your blood vessels so your heart doesn't work as hard.",
                warning: ""
              },
              {
                name: "Potassium Chloride - 20 mEq",
                nickname: "Mineral booster",
                timing: "Take 1 pill every morning with food",
                purpose: "Replaces natural minerals that wash out when taking water pills.",
                warning: "Swallow whole with food. Do not chew or crush."
              }
            ],
            dailyRules: [
              "Weigh yourself every single morning right after using the bathroom and before eating breakfast. Write down the number.",
              "Drink no more than 6 small cups of fluid (water, juice, soup, ice) each day.",
              "Do not add table salt to your food and avoid salty canned or fast food."
            ],
            warningSigns: [
              "You gain 3 pounds in one day OR 5 pounds in one week on your scale",
              "You wake up at night gasping for breath or need extra pillows to sleep",
              "Your feet, ankles, or belly get visibly swollen again",
              "You feel dizzy, faint, or have chest pain"
            ],
            followUp: [
              "Blood test at the clinic lab in 5 days (Tuesday) to check kidney health",
              "Follow-up visit with Dr. Lin in 7 days (September 30 at 10:30 AM)"
            ]
          },
          "standard": {
            overview: "You were treated for a heart failure flare-up where fluid accumulated in your lungs and lower legs. After treatment to remove 4.2 liters of fluid, your breathing and kidney functions are stable. Following your medication schedule, daily weigh-ins, and sodium limits is critical to staying healthy and out of the hospital.",
            medications: [
              {
                name: "Furosemide (Lasix) 40 mg",
                nickname: "Diuretic / Water medication",
                timing: "1 tablet by mouth daily at 8:00 AM",
                purpose: "Removes excess fluid through urination to prevent lung congestion.",
                warning: "Take in the morning. Avoid evening doses to prevent disrupted sleep."
              },
              {
                name: "Carvedilol 6.25 mg",
                nickname: "Beta-blocker",
                timing: "1 tablet by mouth twice daily (8:00 AM and 6:00 PM)",
                purpose: "Slows heart rate and reduces the workload on your heart muscle.",
                warning: "Take with breakfast and dinner."
              },
              {
                name: "Lisinopril 10 mg",
                nickname: "ACE inhibitor",
                timing: "1 tablet by mouth once daily in the morning",
                purpose: "Lowers blood pressure and protects your heart and kidney tissues.",
                warning: "Report any persistent dry cough or dizziness."
              },
              {
                name: "Potassium Chloride 20 mEq",
                nickname: "Electrolyte supplement",
                timing: "1 tablet by mouth daily with breakfast",
                purpose: "Replenishes potassium lost from diuretic therapy.",
                warning: "Take with food and a full glass of water."
              }
            ],
            dailyRules: [
              "Daily Weight: Weigh yourself every morning after urinating, before eating, wearing similar clothing. Keep a daily log.",
              "Fluid Restriction: Limit all liquids to 1,500 mL (approx. 50 oz or 6 cups) per day.",
              "Low-Sodium Diet: Keep dietary sodium under 2,000 mg per day. Read food nutrition labels carefully."
            ],
            warningSigns: [
              "Sudden weight gain: 3 lbs or more in 24 hours, or 5 lbs or more in 1 week",
              "Shortness of breath while lying flat or walking short distances",
              "New or worsening swelling in your ankles, legs, or abdomen",
              "Dizziness, lightheadedness, or sudden chest pain (Call 911)"
            ],
            followUp: [
              "Metabolic blood test (BMP): In 5 days at Metropolitan Hospital Outpatient Lab",
              "Cardiology check-up with Dr. Sarah Lin: September 30, 2026 at 10:30 AM"
            ]
          },
          "advanced": {
            overview: "Discharge protocol for acute decompensated heart failure with reduced ejection fraction (HFrEF, EF ~32%). Euvolemic state achieved following 4.2L diuresis with stable creatinine (1.05 mg/dL). Management now transitions to oral maintenance therapy with guideline-directed neurohormonal blockade and strict volume management.",
            medications: [
              {
                name: "Furosemide (Lasix) 40 mg PO qAM",
                nickname: "Loop diuretic maintenance",
                timing: "Daily morning dose (08:00)",
                purpose: "Promotes renal sodium and water clearance to maintain target euvolemia.",
                warning: "Coordinate with potassium supplementation; monitor for orthostasis."
              },
              {
                name: "Carvedilol 6.25 mg PO BID",
                nickname: "Non-selective beta/alpha-1 adrenergic antagonist",
                timing: "08:00 and 18:00 with food",
                purpose: "Cardioprotection, reduction of myocardial oxygen demand, rate control.",
                warning: "Do not abruptly discontinue; take with meals to reduce postural hypotension."
              },
              {
                name: "Lisinopril 10 mg PO daily",
                nickname: "Angiotensin-converting enzyme (ACE) inhibitor",
                timing: "Daily morning (08:00)",
                purpose: "Afterload reduction and suppression of adverse ventricular remodeling.",
                warning: "Report angioedema symptoms immediately."
              },
              {
                name: "Potassium Chloride 20 mEq PO daily",
                nickname: "Electrolyte replacement",
                timing: "Daily with morning meal",
                purpose: "Offsets kaliuretic losses from loop diuretic regimen.",
                warning: "Lab check scheduled in 5 days to confirm target K+ between 4.0-5.0 mEq/L."
              }
            ],
            dailyRules: [
              "Precision Weight Protocol: Baseline dry weight established at 85.2 kg. Record every morning post-voiding.",
              "Strict 1.5 L/day Fluid Cap: Encompasses all beverages, soups, and gelatin products.",
              "Sodium Restriction (<2,000 mg/day): Eliminates fluid retention secondary to hyperosmolarity."
            ],
            warningSigns: [
              "Weight fluctuation >= 3 lbs/24h or >= 5 lbs/7d indicating subclinical fluid retention",
              "Orthopnea progression or paroxysmal nocturnal dyspnea (PND)",
              "Peripheral pitting edema reaccumulation",
              "Hypotension/syncope or acute anginal symptoms"
            ],
            followUp: [
              "BMP (Serum Creatinine, BUN, K+, Na+) in 5 days",
              "Heart Failure Specialty Clinic appointment: Sept 30, 2026 at 10:30 AM"
            ]
          }
        },
        "es": {
          "basic": {
            overview: "Usted vino al hospital porque su corazón no podía sacar el exceso de agua del cuerpo y le costaba respirar. Le dimos medicina para eliminar el líquido y ahora puede descansar seguro en casa.",
            medications: [
              {
                name: "Furosemida (Lasix) - 40 mg",
                nickname: "Pastilla para eliminar agua",
                timing: "Tome 1 pastilla cada mañana a las 8:00 AM con agua",
                purpose: "Ayuda a sacar el líquido de más para que no se le vaya a los pulmones.",
                warning: "Tómela en la mañana para no levantarse de noche al baño."
              },
              {
                name: "Carvedilol - 6.25 mg",
                nickname: "Protector del corazón",
                timing: "Tome 1 pastilla dos veces al día (desayuno y cena)",
                purpose: "Ayuda a que el corazón lata con calma y baja la presión.",
                warning: "Tómela siempre con comida para no marearse."
              },
              {
                name: "Lisinopril - 10 mg",
                nickname: "Pastilla para la presión",
                timing: "Tome 1 pastilla al día por la mañana",
                purpose: "Relaja las arterias para que el corazón trabaje menos.",
                warning: ""
              },
              {
                name: "Cloruro de Potasio - 20 mEq",
                nickname: "Mineral protector",
                timing: "Tome 1 pastilla con el desayuno",
                purpose: "Repone los minerales perdidos al orinar.",
                warning: "Trague la pastilla entera con agua."
              }
            ],
            dailyRules: [
              "Pésese cada mañana en ayunas después de ir al baño. Anote el número.",
              "No tome más de 6 vasos pequeños de líquido al día.",
              "No agregue sal a sus comidas y evite comida enlatada o frita."
            ],
            warningSigns: [
              "Sube 3 libras en un día o 5 libras en una semana",
              "Se despierta con falta de aire o necesita más almohadas para dormir",
              "Pies, piernas o panza se vuelven a hinchar",
              "Mareo fuerte, desmayo o dolor de pecho"
            ],
            followUp: [
              "Análisis de sangre en el laboratorio en 5 días",
              "Cita con la Dra. Lin en 7 días (30 de Septiembre a las 10:30 AM)"
            ]
          },
          "standard": {
            overview: "Usted recibió tratamiento en el hospital debido a una acumulación de líquido en sus pulmones y piernas a causa de su corazón (insuficiencia cardíaca). Logramos eliminar 4.2 litros de líquido extra y ahora su respiración y riñones están estables. Es muy importante tomar sus medicamentos a tiempo, pesarse todos los días y cuidar el consumo de sal.",
            medications: [
              {
                name: "Furosemida (Lasix) 40 mg",
                nickname: "Pastilla para eliminar líquidos",
                timing: "1 tableta por la mañana a las 8:00 AM",
                purpose: "Le ayuda a orinar el exceso de líquido para que no se acumule en sus pulmones.",
                warning: "Tómela en la mañana para no tener que levantarse al baño de noche."
              },
              {
                name: "Carvedilol 6.25 mg",
                nickname: "Protector del corazón",
                timing: "1 tableta dos veces al día con alimentos (8:00 AM y 6:00 PM)",
                purpose: "Ayuda a que el corazón lata con calma y baja la presión.",
                warning: "Tómela siempre con el desayuno y la cena."
              },
              {
                name: "Lisinopril 10 mg",
                nickname: "Medicamento para la presión arterial",
                timing: "1 tableta al día por la mañana",
                purpose: "Relaja las arterias para que el corazón no trabaje con tanto esfuerzo.",
                warning: "Avise al médico si presenta tos seca persistente."
              },
              {
                name: "Cloruro de Potasio 20 mEq",
                nickname: "Suplemento de potasio",
                timing: "1 tableta al día con el desayuno",
                purpose: "Repone los minerales que se pierden con la pastilla de orina.",
                warning: "Trague la tableta entera con un vaso lleno de agua."
              }
            ],
            dailyRules: [
              "Pésese cada mañana al levantarse, después de orinar y antes del desayuno. Anote su peso.",
              "Límite de líquidos: No tome más de 1,500 mL (unas 6 tazas) de líquido al día.",
              "Dieta baja en sal: Consuma menos de 2,000 mg de sodio al día. Evite embutidos y comida chatarra."
            ],
            warningSigns: [
              "Aumento rápido de peso: 3 libras en 24 horas o 5 libras en una semana",
              "Falta de aire al acostarse o necesidad de dormir con varias almohadas",
              "Hinchazón notable en los tobillos, piernas o abdomen",
              "Mareos intensos, desmayos o dolor en el pecho (Llame al 911)"
            ],
            followUp: [
              "Análisis de sangre en el laboratorio en 5 días",
              "Cita de control con la Dra. Lin: 30 de Septiembre a las 10:30 AM"
            ]
          },
          "advanced": {
            overview: "Protocolo de alta hospitalaria para insuficiencia cardíaca aguda descompensada con fracción de eyección reducida (ICFEr 32%). Se logró la euvolemia tras diuresis de 4.2 L con creatinina sérica estable (1.05 mg/dL). Se requiere adherencia estricta a la terapia con neurohormonales y control volumétrico.",
            medications: [
              {
                name: "Furosemida (Lasix) 40 mg VO matutino",
                nickname: "Diurético de asa de mantenimiento",
                timing: "Dosis diaria matutina (08:00)",
                purpose: "Favorece la eliminación de sodio y agua para mantener la euvolemia.",
                warning: "Coordinar con aporte de potasio; vigilar hipotensión ortostática."
              },
              {
                name: "Carvedilol 6.25 mg VO cada 12h",
                nickname: "Antagonista adrenérgico neurohormonal",
                timing: "08:00 y 18:00 con alimentos",
                purpose: "Cardioprotección y control de la frecuencia cardíaca.",
                warning: "No suspender bruscamente; tomar con comidas."
              }
            ],
            dailyRules: [
              "Registro de peso basal estricto cada mañana tras micción matutina.",
              "Restricción de líquidos: Límite estricto de 1,500 mL/día.",
              "Restricción de sodio: Menos de 2,000 mg/día."
            ],
            warningSigns: [
              "Aumento ponderal >= 3 lbs en 24h o >= 5 lbs en 7 días",
              "Ortopnea progresiva o disnea paroxística nocturna",
              "Reaparición de edema maleolar con fóvea",
              "Presíncope o angina aguda"
            ],
            followUp: [
              "Panel metabólico básico (BMP) en 5 días",
              "Consulta de seguimiento con Dra. Sarah Lin en 7 días"
            ]
          }
        },
        "zh": {
          "standard": {
            overview: "您因心脏功能减弱导致体内积水（心力衰竭急性发作）而住院治疗。经过治疗，已顺利排出4.2升多余水分，目前呼吸顺畅、肾功能稳定。出院后，请务必按时服药、每天称体重并严格控制盐和水分摄入。",
            medications: [
              {
                name: "呋塞米片 (Furosemide / Lasix) 40毫克",
                nickname: "利尿消肿药",
                timing: "每天早晨 8:00 口服 1 片",
                purpose: "帮助身体排出多余水分，防止肺部积水。",
                warning: "请在早晨服用，避免夜间频繁起夜影响睡眠。"
              },
              {
                name: "卡维地洛片 (Carvedilol) 6.25毫克",
                nickname: "护心降压药",
                timing: "每天 2 次，随早餐和晚餐服用 (8:00 和 18:00)",
                purpose: "减轻心脏负担，保护心肌功能。",
                warning: "必须随餐服用以防头晕。"
              },
              {
                name: "赖诺普利片 (Lisinopril) 10毫克",
                nickname: "血管舒张药",
                timing: "每天早晨 1 次，口服 1 片",
                purpose: "控制血压，保护心脏和肾脏。",
                warning: "若有持续干咳请告知医生。"
              },
              {
                name: "氯化钾缓释片 20 mEq",
                nickname: "补钾药",
                timing: "每天早晨随餐服用 1 片",
                purpose: "补充因利尿剂排出的体内钾离子。",
                warning: "请整片吞服，切勿咀嚼或压碎。"
              }
            ],
            dailyRules: [
              "每日早晨称重：排尿后、吃早饭前，穿着轻便衣物称重并记录数值。",
              "严格限制水分：每天饮水及汤饮总量不得超过1500毫升（约6杯水）。",
              "严格低盐饮食：每天盐摄入量低于2000毫克，少吃咸菜和腌制品。"
            ],
            warningSigns: [
              "体重快速增加：24小时内增加超过3磅（约1.4公斤）或一周增加5磅",
              "平躺时呼吸困难，需要垫高枕头才能入睡",
              "脚踝、双腿或腹部出现明显水肿",
              "突发胸痛、严重眩晕或昏厥（请立即拨打911）"
            ],
            followUp: [
              "5天后前往门诊化验室进行基础代谢与肾功能验血 (BMP)",
              "7天后（9月30日上午10:30）回心内科复诊 Sarah Lin 医生"
            ]
          }
        },
        "vi": {
          "standard": {
            overview: "Quý vị đã được điều trị vì suy tim ứ dịch khiến phổi khó thở và sưng phù hai chân. Sau khi loại bỏ 4.2 lít dịch thừa, hiện tại sức khỏe đã ổn định. Quý vị cần uống thuốc đúng giờ, tự cân mỗi ngày và giảm muối để bảo vệ tim.",
            medications: [
              {
                name: "Furosemide (Lasix) 40 mg",
                nickname: "Thuốc lợi tiểu / Thải nước",
                timing: "Uống 1 viên vào 8:00 sáng mỗi ngày",
                purpose: "Giúp bài tiết nước dư thừa qua đường tiểu để tránh tràn dịch phổi.",
                warning: "Uống buổi sáng để tránh đi tiểu đêm làm mất giấc ngủ."
              },
              {
                name: "Carvedilol 6.25 mg",
                nickname: "Thuốc bảo vệ tim mạch",
                timing: "Uống 1 viên x 2 lần mỗi ngày cùng bữa ăn (8:00 sáng và 6:00 chiều)",
                purpose: "Giúp nhịp tim đập êm và giảm bớt gánh nặng cho cơ tim.",
                warning: "Uống kèm khi ăn để tránh chóng mặt."
              }
            ],
            dailyRules: [
              "Cân đo mỗi sáng: Cân ngay sau khi đi tiểu và trước khi ăn sáng. Ghi chép số cân.",
              "Hạn chế nước uống: Không quá 1,500 mL (khoảng 6 ly nhỏ) mỗi ngày.",
              "Ăn nhạt ít muối: Dưới 2,000 mg muối mỗi ngày, tránh đồ hộp và mắm mặn."
            ],
            warningSigns: [
              "Tăng cân đột ngột: Tăng 3 lbs trong 24 giờ hoặc 5 lbs trong 1 tuần",
              "Khó thở khi nằm thẳng, phải kê cao gối mới ngủ được",
              "Hai chân hoặc bụng sưng to trở lại",
              "Chóng mặt nặng hoặc đau thắt ngực (Gọi cấp cứu 911)"
            ],
            followUp: [
              "Xét nghiệm máu sau 5 ngày tại phòng khám",
              "Tái khám với Bác sĩ Sarah Lin vào ngày 30 tháng 9 lúc 10:30 AM"
            ]
          }
        },
        "tl": {
          "standard": {
            overview: "Ginamot kayo sa ospital dahil sa pagkaipon ng labis na tubig sa inyong baga at mga binti dulot ng panghihina ng puso. Matapos maalis ang 4.2 litrong tubig, maayos na po ang inyong paghinga at bato. Napakahalagang inumin ang inyong mga gamot sa tamang oras, magtimbang araw-araw, at magbawas ng maalat.",
            medications: [
              {
                name: "Furosemide (Lasix) 40 mg",
                nickname: "Pang-ihi / Pampabawas ng tubig",
                timing: "1 tableta bawat umaga sa ganap na 8:00 AM",
                purpose: "Tumutulong umihi upang maalis ang sobrang tubig at hindi maipon sa baga.",
                warning: "Inumin sa umaga upang hindi magpabalik-balik sa banyo sa gabi."
              },
              {
                name: "Carvedilol 6.25 mg",
                nickname: "Proteksyon sa puso",
                timing: "1 tableta dalawang beses sa isang araw kasabay ng pagkain (8:00 AM at 6:00 PM)",
                purpose: "Tumutulong na maging banayad ang tibok ng puso at mapababa ang presyon.",
                warning: "Inumin kasabay ng agahan at hapunan upang hindi mahilo."
              }
            ],
            dailyRules: [
              "Araw-araw na pagtimbang: Magtimbang tuwing umaga pagkagising pagkatapos umihi at bago kumain.",
              "Limitasyon sa tubig: Hanggang 1,500 mL (mga 6 na baso) lamang ang inumin sa buong araw.",
              "Bawasan ang asin: Iwasan ang maaalat na sawsawan, tuyo, at de-lata."
            ],
            warningSigns: [
              "Biglaang pagbigat ng timbang: 3 lbs sa 24 oras o 5 lbs sa isang linggo",
              "Hirap huminga kapag nakahiga nang patag o kailangang magpatong ng unan",
              "Pamamaga muli ng mga bukong-bukong at binti",
              "Matinding pagkahilo o paninikip ng dibdib (Tumawag agad sa 911)"
            ],
            followUp: [
              "Pagsusuri sa dugo (BMP) sa laboratoryo pagkalipas ng 5 araw",
              "Pagpapatingin kay Dr. Sarah Lin sa Setyembre 30 sa ganap na 10:30 AM"
            ]
          }
        },
        "ar": {
          "standard": {
            overview: "تم علاجك في المستشفى بسبب تجمع السوائل الزائدة في الرئتين والساقين نتيجة ضعف عضلة القلب. بعد تفريغ 4.2 لتر من السوائل الزائدة، أصبحت وظائف التنفس والكلى مستقرة الآن. من الضروري جداً الالتزام بمواعيد الأدوية، وقياس الوزن يومياً، وتقليل الأملاح.",
            medications: [
              {
                name: "فوروسيميد (لازيكس) 40 ملغ",
                nickname: "مدر البول / طارد السوائل",
                timing: "قرص واحد كل صباح في الساعة 8:00 صباحاً",
                purpose: "يساعد الجسم على التخلص من الماء الزائد لمنع احتقان الرئتين.",
                warning: "تناوله صباحاً لتجنب الاستيقاظ ليلاً للذهاب إلى الحمام."
              },
              {
                name: "كارفيديلول 6.25 ملغ",
                nickname: "حامي القلب وخافض الضغط",
                timing: "قرص واحد مرتين يومياً مع وجبات الطعام (8:00 صباحاً و 6:00 مساءً)",
                purpose: "يساعد القلب على النبض بهدوء ويقلل الجهد المبذول.",
                warning: "تناوله مع الطعام لتفادي الشعور بالدوار."
              }
            ],
            dailyRules: [
              "قياس الوزن يومياً: قس وزنك كل صباح بعد التبول وقبل الإفطار وسجل القراءة.",
              "تحديد كمية السوائل: لا تشرب أكثر من 1500 مل (حوالي 6 أكواب) من جميع السوائل يومياً.",
              "تقليل الملح: تجنب الأطعمة المالحة والمعلبات والوجبات السريعة."
            ],
            warningSigns: [
              "زيادة سريعة في الوزن: 3 أرطال في 24 ساعة أو 5 أرطال في أسبوع",
              "صعوبة في التنفس أثناء الاستلقاء أو الحاجة لوسائد إضافية للنوم",
              "انتفاخ جديد أو متزايد في القدمين أو الساقين",
              "دوار شديد، إغماء، أو ألم في الصدر (اتصل بالطوارئ 911 فوراً)"
            ],
            followUp: [
              "فحص دم في المختبر بعد 5 أيام لفحص وظائف الكلى والأملاح",
              "موعد متابعة مع الدكتورة سارة لين في 30 سبتمبر الساعة 10:30 صباحاً"
            ]
          }
        },
        "fr": {
          "standard": {
            overview: "Vous avez été traité à l'hôpital pour une décompensation cardiaque où du liquide s'est accumulé dans vos poumons et vos jambes. Après avoir évacué 4,2 litres de liquide superflu, votre respiration et votre fonction rénale sont stables. Il est essentiel de respecter scrupuleusement vos prises de médicaments, vos pesées quotidiennes et la restriction en sel.",
            medications: [
              {
                name: "Furosémide (Lasix) 40 mg",
                nickname: "Diurétique / Éliminateur d'eau",
                timing: "1 comprimé le matin à 8h00 avec de l'eau",
                purpose: "Élimine l'excès d'eau par l'urine pour prévenir la congestion pulmonaire.",
                warning: "Prenez-le le matin pour éviter de vous lever la nuit."
              },
              {
                name: "Carvédilol 6,25 mg",
                nickname: "Bêtabloquant protecteur",
                timing: "1 comprimé 2 fois par jour aux repas (8h00 et 18h00)",
                purpose: "Ralentit le rythme cardiaque et soulage le muscle cardiaque.",
                warning: "À prendre impérativement pendant les repas."
              },
              {
                name: "Lisinopril 10 mg",
                nickname: "Inhibiteur de l'ECA",
                timing: "1 comprimé une fois par jour le matin",
                purpose: "Baisse la pression artérielle et protège le cœur et les reins.",
                warning: "Signalez toute toux sèche persistante."
              },
              {
                name: "Chlorure de Potassium 20 mEq",
                nickname: "Supplément de potassium",
                timing: "1 comprimé par jour au petit-déjeuner",
                purpose: "Compense les pertes en potassium causées par le diurétique.",
                warning: "Avaler entier avec un grand verre d'eau."
              }
            ],
            dailyRules: [
              "Pesée quotidienne : Pesez-vous chaque matin après avoir uriné et avant le petit-déjeuner. Notez votre poids.",
              "Restriction hydrique : Limitez tous les liquides à 1 500 mL (environ 6 verres) par jour.",
              "Régime pauvre en sel : Moins de 2 000 mg de sodium par jour. Évitez les plats préparés et salés."
            ],
            warningSigns: [
              "Prise de poids rapide : plus de 1,5 kg en 24h ou 2,3 kg en une semaine",
              "Essoufflement en position allongée ou lors de petits efforts",
              "Gonflement nouveau ou aggravé des chevilles ou des jambes",
              "Vertiges graves ou douleur thoracique (Appelez le 15 ou le 112)"
            ],
            followUp: [
              "Prise de sang au laboratoire dans 5 jours (bilan ionique)",
              "Consultation de cardiologie avec le Dr Sarah Lin le 30 septembre à 10h30"
            ]
          }
        },
        "hi": {
          "standard": {
            overview: "आपके फेफड़ों और पैरों में अतिरिक्त पानी जमा होने के कारण अस्पताल में आपका इलाज किया गया (हार्ट फेलियर)। 4.2 लीटर अतिरिक्त पानी निकाले जाने के बाद अब आपकी सांस और किडनी की स्थिति स्थिर है। घर पर अपनी दवाएं समय पर लेना, रोज सुबह वजन नापना और नमक कम खाना अत्यंत आवश्यक है।",
            medications: [
              {
                name: "फ़्यूरोसेमाइड (Lasix) 40 mg",
                nickname: "पेशाब की गोली / पानी निकालने वाली दवा",
                timing: "रोजाना सुबह 8:00 बजे पानी के साथ 1 गोली",
                purpose: "शरीर से अतिरिक्त पानी बाहर निकालती है ताकि फेफड़ों में पानी न भरे।",
                warning: "इसे सुबह ही लें ताकि रात में बार-बार पेशाब के लिए न उठना पड़े।"
              },
              {
                name: "कार्वेडिलोल 6.25 mg",
                nickname: "हृदय रक्षक दवा",
                timing: "दिन में 2 बार भोजन के साथ (सुबह 8:00 और शाम 6:00 बजे)",
                purpose: "दिल की धड़कन को नियंत्रित रखती है और रक्तचाप को संतुलित करती है।",
                warning: "चक्कर आने से बचने के लिए हमेशा भोजन के साथ लें।"
              }
            ],
            dailyRules: [
              "रोजाना सुबह वजन नापें: शौच के बाद और नाश्ते से पहले वजन नापें और डायरी में लिखें।",
              "तरल पदार्थों की सीमा: दिन भर में 1500 मिलीलीटर (लगभग 6 छोटे गिलास) से अधिक पानी या तरल न पिएं।",
              "कम नमक का आहार: भोजन में ऊपर से नमक न डालें और नमकीन व डिब्बाबंद खाद्य पदार्थों से बचें।"
            ],
            warningSigns: [
              "अचानक वजन बढ़ना: 24 घंटे में 3 पाउंड (1.5 किग्रा) या एक हफ्ते में 5 पाउंड बढ़ना",
              "सीधे लेटने पर सांस फूलना या सोने के लिए ज्यादा तकियों की जरूरत पड़ना",
              "पैरों या टखनों में फिर से सूजन आना",
              "अत्यधिक चक्कर आना या सीने में दर्द होना (तुरंत 911 या नजदीकी आपातकालीन सेवा को कॉल करें)"
            ],
            followUp: [
              "5 दिनों में लैब में रक्त परीक्षण (BMP - इलेक्ट्रोलाइट्स व किडनी जांच)",
              "7 दिनों में (30 सितंबर सुबह 10:30 बजे) डॉ. सारा लिन के साथ फॉलो-अप"
            ]
          }
        }
      },

      // Factual Consistency Audit Details
      factualAudit: {
        status: "verified", // verified | review | mismatch
        score: "100%",
        summary: "All 4 active medications, exact dosages, frequency, fluid limits, and follow-up lab dates match the clinical summary with zero hallucinations or omissions.",
        checks: [
          { item: "Medication Dosing Check", status: "pass", detail: "Furosemide 40mg PO qAM, Lisinopril 10mg, Carvedilol 6.25mg BID, Klor-Con 20mEq verified." },
          { item: "Clinical Allergy Cross-Check", status: "pass", detail: "No known drug allergies (NKDA) in record; no contraindications flagged." },
          { item: "Numerical Threshold Check", status: "pass", detail: "Fluid restriction 1500mL, Na+ limit <2000mg, Weight alert >3lbs/24h accurately matched." },
          { item: "Follow-up Timeline Check", status: "pass", detail: "BMP lab in 5 days, Clinic visit with Dr. Lin in 7 days (09/30/2026) verified." }
        ]
      },

      // Readability comparison
      readability: {
        original: {
          gradeLevel: "College Senior (Grade 15.2)",
          fleschReadingEase: 24.8, // 0 - 100
          jargonDensity: "41.5%",
          avgSentenceLength: "22.4 words",
          tone: "Dense Medical / Acronyms"
        },
        generated: {
          gradeLevel: "5th Grade (Grade 5.3)",
          fleschReadingEase: 88.6, // High is easy
          jargonDensity: "2.1%",
          avgSentenceLength: "9.2 words",
          tone: "Clear, Actionable, Empathetic"
        },
        vocabularyTranslation: [
          { medical: "Acute decompensated heart failure", patient: "Heart failure flare-up with extra fluid buildup" },
          { medical: "Dyspnea on exertion / Orthopnea", patient: "Trouble breathing when walking or lying flat" },
          { medical: "Bilateral lower extremity edema", patient: "Swelling in both feet and ankles" },
          { medical: "Loop Diuretic (Furosemide)", patient: "Water pill that helps you pee out extra fluid" },
          { medical: "Euvolemic status", patient: "Safe, healthy fluid balance in the body" }
        ]
      }
    },

    {
      id: "diabetes_cellulitis",
      title: "Type 2 Diabetes & Lower Extremity Cellulitis",
      category: "Endocrinology / Infectious Disease",
      tag: "Verified",
      patientInfo: {
        name: "Maria Santos",
        age: 54,
        mrn: "MRN-391084",
        admissionDate: "2026-09-22",
        dischargeDate: "2026-09-24",
        attending: "Dr. Sarah Lin, MD"
      },
      originalNote: `DISCHARGE SUMMARY
PATIENT: Santos, Maria | MRN: 391084 | AGE: 54 | SEX: F
ATTENDING: Sarah Lin, MD | ADMIT: 09/22/2026 | DISCHARGE: 09/24/2026

PRIMARY DIAGNOSES:
1. Right lower extremity cellulitis (MSSA bacteremia ruled out).
2. Uncontrolled Type 2 Diabetes Mellitus with transient hyperglycemia (HbA1c 9.4%).

CLINICAL COURSE:
Patient admitted with right calf erythema, warmth, and localized tenderness spreading 8cm from distal abrasion. Blood cultures x2 negative. Received IV Cefazolin 1g q8h with marked reduction in erythema borders. Transitioning to oral antibiotic regimen for 10-day outpatient course. Metformin temporarily held during IV contrast CT, now resumed. Glipizide discontinued due to hypoglycemia risk; insulin glargine initiated.

DISCHARGE MEDICATIONS:
1. Cephalexin (Keflex) 500 mg PO four times daily (QID: 08:00, 12:00, 16:00, 20:00) with food for 10 days. FINISH ENTIRE COURSE.
2. Metformin 500 mg PO twice daily with morning and evening meals.
3. Insulin Glargine (Lantus) 14 units SubQ once daily at bedtime (21:00).
4. Acetaminophen 650 mg PO q6h PRN for right leg pain. Avoid NSAIDs (Ibuprofen/Naproxen).

WOUND CARE & ACTIVITY:
- Elevate right lower extremity on 2 pillows above heart level when seated or in bed.
- Keep abrasion clean and dry. Wash gently with mild soap, pat dry, apply sterile dry dressing daily.
- Draw line with surgical pen around red border; if erythema crosses border or streaking occurs, contact clinic.
- Blood Glucose monitoring: Check fasting AM and post-prandial glucose. Target fasting: 90-130 mg/dL.

FOLLOW-UP:
- Primary Care Clinic in 7 days for leg wound check.
- Certified Diabetes Educator (CDE) consult scheduled for 10/05/2026.`,
      
      translations: {
        "en": {
          "basic": {
            overview: "You came to the hospital for a skin infection (cellulitis) in your right leg and high blood sugar. The swelling and redness improved with medicine, and you are ready to continue healing at home with antibiotic pills and blood sugar support.",
            medications: [
              {
                name: "Cephalexin (Keflex) - 500 mg",
                nickname: "Antibiotic infection fighter",
                timing: "Take 1 pill 4 times a day (breakfast, lunch, dinner, bedtime) for 10 full days",
                purpose: "Kills the germs causing the skin infection.",
                warning: "Finish ALL pills even if your leg looks completely healed!"
              },
              {
                name: "Metformin - 500 mg",
                nickname: "Blood sugar pill",
                timing: "Take 1 pill two times a day with meals (breakfast & dinner)",
                purpose: "Keeps your daily sugar levels steady.",
                warning: "Always take with food to protect your stomach."
              },
              {
                name: "Insulin Glargine (Lantus)",
                nickname: "Bedtime insulin shot",
                timing: "Inject 14 units under the skin every night at 9:00 PM",
                purpose: "Provides gentle, all-night blood sugar control.",
                warning: "Keep refrigerated until open. Rotate injection spots on your belly."
              }
            ],
            dailyRules: [
              "Prop your right leg up on 2 pillows whenever resting so it stays higher than your heart.",
              "Wash the leg wound gently with mild soap and water, pat dry, and cover with clean gauze daily.",
              "Check your blood sugar every morning before breakfast. Aim for 90 to 130."
            ],
            warningSigns: [
              "The redness spreads past the pen mark on your leg",
              "You develop fever, chills, or pus leaking from the skin",
              "Blood sugar drops below 70 (shakiness, cold sweat, hunger) - drink half cup juice immediately",
              "Severe or worsening leg pain"
            ],
            followUp: [
              "Visit clinic in 7 days to check how your leg is healing",
              "Meeting with diabetes educator on October 5th"
            ]
          },
          "standard": {
            overview: "You were hospitalized for right leg cellulitis (a bacterial skin infection) and elevated blood sugar. The infection responded well to IV antibiotics and is now transitioning to oral antibiotics for 10 days. In addition, your diabetes regimen has been updated with bedtime insulin to improve blood sugar control while your body recovers.",
            medications: [
              {
                name: "Cephalexin (Keflex) 500 mg",
                nickname: "Oral Antibiotic",
                timing: "1 capsule by mouth 4 times daily (approx. every 6 hours) for 10 days",
                purpose: "Eradicates remaining bacterial infection in the skin tissue.",
                warning: "Complete the entire 10-day prescription without missing doses."
              },
              {
                name: "Metformin 500 mg",
                nickname: "Oral hypoglycemic",
                timing: "1 tablet by mouth twice daily with morning and evening meals",
                purpose: "Improves insulin sensitivity and lowers hepatic glucose output.",
                warning: "Take with food to minimize gastrointestinal upset."
              },
              {
                name: "Insulin Glargine (Lantus) 14 Units",
                nickname: "Long-acting basal insulin",
                timing: "Inject 14 units subcutaneously once daily at 9:00 PM bedtime",
                purpose: "Stabilizes baseline blood glucose overnight and between meals.",
                warning: "Always use a new needle; rotate injection sites across abdomen/thighs."
              }
            ],
            dailyRules: [
              "Leg Elevation: Elevate right leg above heart level for at least 30 minutes 3-4 times a day.",
              "Wound Care: Daily gentle wash, air dry, and clean dressing. Inspect daily for spreading redness.",
              "Glucose Monitoring: Fasting morning check (goal 90-130 mg/dL) and before bedtime."
            ],
            warningSigns: [
              "Erythema spreading beyond marked border or red streaks extending up the leg",
              "Fever > 100.4°F (38°C), chills, or nausea",
              "Hypoglycemia (< 70 mg/dL): treat immediately with 15g fast-acting carbs (juice/glucose tabs)",
              "Unrelieved severe pain or blister formation"
            ],
            followUp: [
              "Primary Care Clinic: 7-day wound re-evaluation",
              "Diabetes Educator Consultation: Scheduled for October 5, 2026"
            ]
          },
          "advanced": {
            overview: "Resolution of acute right lower extremity cellulitis with transition from intravenous cefazolin to a 10-day course of high-dose cephalexin. Glycemic management recalibrated secondary to stress-induced hyperglycemia and HbA1c of 9.4%, introducing basal insulin glargine while restarting metformin.",
            medications: [
              {
                name: "Cephalexin 500 mg PO QID",
                nickname: "First-generation cephalosporin",
                timing: "q6h (08:00, 12:00, 16:00, 20:00) with meals/snacks x 10 days",
                purpose: "Gram-positive coverage against methicillin-susceptible Staphylococcus & Streptococcus.",
                warning: "Mandatory completion of 10-day regimen to prevent recrudescence."
              },
              {
                name: "Metformin 500 mg PO BID",
                nickname: "Biguanide antihyperglycemic",
                timing: "Twice daily with meals",
                purpose: "Hepatic gluconeogenesis reduction.",
                warning: "Discontinue if acute systemic illness or dehydration occurs."
              },
              {
                name: "Insulin Glargine 14 Units SubQ qHS",
                nickname: "Basal insulin analogue",
                timing: "Bedtime (21:00)",
                purpose: "Basal coverage without pronounced peak effect.",
                warning: "Carry fast-acting oral glucose; log morning fasting capillary blood glucose."
              }
            ],
            dailyRules: [
              "Venous Drainage Elevation: 30-45 degree elevation above right atrium.",
              "Border Surveillance: Maintain demarcation line; inspect for ascending lymphangitis.",
              "Glycemic Targets: Fasting 90-130 mg/dL; 2-hour postprandial < 180 mg/dL."
            ],
            warningSigns: [
              "Expansion of erythematous margin or systemic signs of SIRS",
              "Bullae, crepitus, or skin necrosis",
              "Refractory hypoglycemia or ketonuria"
            ],
            followUp: [
              "PCP follow-up within 7 calendar days for cellulitis resolution audit",
              "Comprehensive CDE diabetes education visit on October 5, 2026"
            ]
          }
        },
        "es": {
          "standard": {
            overview: "Usted estuvo hospitalizada por una infección en la piel (celulitis) en la pierna derecha y niveles altos de azúcar. La infección mejoró notablemente con antibióticos y ahora puede continuar su tratamiento en casa con pastillas e insulina para controlar la glucosa.",
            medications: [
              {
                name: "Cefalexina (Keflex) 500 mg",
                nickname: "Antibiótico para la piel",
                timing: "1 cápsula 4 veces al día con comidas por 10 días completos",
                purpose: "Elimina las bacterias que causaron la infección en la pierna.",
                warning: "Termine todo el medicamento aunque la pierna ya no esté roja."
              },
              {
                name: "Metformina 500 mg",
                nickname: "Pastilla para la diabetes",
                timing: "1 tableta dos veces al día con el desayuno y la cena",
                purpose: "Mantiene estable el nivel de azúcar en la sangre.",
                warning: "Tómela siempre con comida para evitar malestar estomacal."
              },
              {
                name: "Insulina Glargina (Lantus) 14 Unidades",
                nickname: "Insulina de la noche",
                timing: "Inyectar 14 unidades bajo la piel todas las noches a las 9:00 PM",
                purpose: "Controla su azúcar de manera suave durante la noche.",
                warning: "Cambie el lugar de la inyección en su abdomen cada noche."
              }
            ],
            dailyRules: [
              "Mantenga la pierna derecha levantada sobre 2 almohadas cuando esté descansando.",
              "Lave suavemente la herida con agua y jabón neutro, seque sin frotar y tape con gasa limpia.",
              "Mida su azúcar cada mañana antes de desayunar (meta: entre 90 y 130)."
            ],
            warningSigns: [
              "El enrojecimiento pasa la línea marcada con pluma en la pierna",
              "Fiebre mayor a 38°C o escalofríos",
              "Baja de azúcar (menor de 70): temblores, sudor frío - tome medio vaso de jugo de inmediato"
            ],
            followUp: [
              "Cita en la clínica en 7 días para revisar la pierna",
              "Consulta con la educadora en diabetes el 5 de Octubre"
            ]
          }
        }
      },

      factualAudit: {
        status: "verified",
        score: "100%",
        summary: "Antibiotic course (Cephalexin 500mg QID x10d), diabetic medications, wound care elevation, and 7-day PCP follow-up match the hospital discharge plan.",
        checks: [
          { item: "Antibiotic Duration & Dosing", status: "pass", detail: "Cephalexin 500mg QID for 10 full days confirmed with complete-course warning." },
          { item: "Insulin & Metformin Safety", status: "pass", detail: "Lantus 14 units at 21:00 and Metformin 500mg BID with meals verified." },
          { item: "Wound Demarcation & Elevation", status: "pass", detail: "Surgical pen demarcation line and 2-pillow leg elevation instructions preserved." },
          { item: "Hypoglycemia Safeguards", status: "pass", detail: "Blood glucose target 90-130 mg/dL and hypoglycemia warning rules incorporated." }
        ]
      },

      readability: {
        original: {
          gradeLevel: "College Junior (Grade 14.6)",
          fleschReadingEase: 28.2,
          jargonDensity: "38.2%",
          avgSentenceLength: "19.8 words",
          tone: "Dense Clinical Notes"
        },
        generated: {
          gradeLevel: "5th Grade (Grade 5.1)",
          fleschReadingEase: 89.4,
          jargonDensity: "1.8%",
          avgSentenceLength: "8.8 words",
          tone: "Direct, Supportive, Simple"
        },
        vocabularyTranslation: [
          { medical: "Cellulitis / Erythema", patient: "Bacterial skin infection with redness and warmth" },
          { medical: "Oral antibiotic regimen (QID)", patient: "Infection-fighting pills taken 4 times a day" },
          { medical: "Subcutaneous insulin glargine", patient: "Gentle once-daily bedtime insulin injection" },
          { medical: "Post-prandial hyperglycemia", patient: "High blood sugar spikes after meals" },
          { medical: "Lymphangitis / Red streaking", patient: "Red lines spreading up the leg" }
        ]
      }
    },

    {
      id: "asthma_pediatric",
      title: "Pediatric Asthma Exacerbation & Inhaler Action Plan",
      category: "Pediatrics / Pulmonology",
      tag: "Verified",
      patientInfo: {
        name: "Lucas Bennett",
        age: 8,
        mrn: "MRN-618402",
        admissionDate: "2026-09-23",
        dischargeDate: "2026-09-24",
        attending: "Dr. Sarah Lin, MD"
      },
      originalNote: `PEDIATRIC DISCHARGE SUMMARY
PATIENT: Bennett, Lucas | AGE: 8yo | SEX: M | MRN: 618402
ADMISSION: 09/23/2026 | DISCHARGE: 09/24/2026 | ATTENDING: Sarah Lin, MD

PRIMARY DIAGNOSIS:
1. Acute moderate asthma exacerbation triggered by viral URI.

CLINICAL COURSE:
8-year-old male with history of moderate persistent asthma presented with acute tachypnea (RR 36), bilateral wheezing, and intercostal retractions. SpO2 91% on room air. Treated with continuous albuterol nebulization x3 and oral dexamethasone. Respiratory distress resolved, oxygen saturation normalized to 98% on RA. Lungs clear to auscultation bilaterally.

DISCHARGE MEDICATIONS:
1. Prednisolone oral solution (15 mg/5 mL): Give 10 mL (30 mg) PO once daily in morning with breakfast for 3 more days (Total 5-day steroid course).
2. Fluticasone propionate (Flovent HFA 44 mcg): 2 puffs inhaled twice daily (morning & night) using AeroChamber spacer. RINSE MOUTH AFTER USE.
3. Albuterol HFA (90 mcg/actuation): 2 puffs inhaled with spacer every 4 to 6 hours as needed for cough or wheezing.
4. Cetirizine (Zyrtec) 5 mg PO daily at bedtime for allergic rhinitis.

ASTHMA ACTION PLAN ZONES:
- GREEN ZONE (Doing Well): No cough or wheeze, sleeps through night. Take Flovent 2 puffs BID.
- YELLOW ZONE (Caution / Flare-up): Cough, mild wheeze, tight chest. Give Albuterol 2 puffs via spacer; repeat in 20 min if needed. If still in yellow after 24h, call pediatrician.
- RED ZONE (Danger / Medical Alert): Hard and fast breathing, ribs pulling in (retractions), difficulty speaking full sentences, blue/gray lips. Give 4 puffs albuterol immediately and call 911.

FOLLOW-UP:
- Pediatrician follow-up in 3 to 5 days with Dr. Chang.`,
      
      translations: {
        "en": {
          "basic": {
            overview: "Lucas had an asthma flare-up caused by a cold virus, which made him cough and have trouble breathing. He received breathing treatments and is now breathing easily. Here is how to keep his lungs healthy and handle any new coughs at home.",
            medications: [
              {
                name: "Prednisolone Liquid (Pink liquid)",
                nickname: "Short steroid medicine",
                timing: "Give 10 mL (2 medicine teaspoons) once each morning with breakfast for 3 days",
                purpose: "Calms down swelling inside his airways.",
                warning: "Give with food to prevent an upset tummy. Only 3 more days needed."
              },
              {
                name: "Flovent Inhaler (Orange puffer)",
                nickname: "Daily controller puffer",
                timing: "2 puffs every morning and 2 puffs every night using his spacer chamber",
                purpose: "Protects his lungs every day so asthma attacks don't happen.",
                warning: "Always have Lucas rinse and spit water after using to prevent mouth sores."
              },
              {
                name: "Albuterol Inhaler (Blue puffer)",
                nickname: "Quick-relief rescue puffer",
                timing: "2 puffs every 4 hours ONLY IF he starts coughing or wheezing",
                purpose: "Quickly opens up the airways if he has trouble breathing.",
                warning: "Always use the clear spacer chamber tube with the puffer."
              }
            ],
            dailyRules: [
              "Always use the clear spacer tube with both inhalers so the medicine reaches deep into his lungs.",
              "Have Lucas gargle and spit warm water after using the orange daily inhaler.",
              "Keep the blue rescue inhaler in his backpack or close to him at all times."
            ],
            warningSigns: [
              "Breathing very fast or stomach/ribs sucking in deeply with each breath",
              "Too out of breath to talk in full sentences or walk across the room",
              "Blue or gray color around his lips, tongue, or fingernails (CALL 911 IMMEDIATELY)",
              "Coughing or wheezing that does not get better 20 minutes after using the blue puffer"
            ],
            followUp: [
              "Pediatrician check-up with Dr. Chang in 3 to 5 days"
            ]
          },
          "standard": {
            overview: "Lucas was treated for a moderate asthma flare-up triggered by a viral respiratory infection. His breathing is now quiet, work of breathing is normal, and oxygen levels are back to 98%. Continued recovery requires finishing the 3-day steroid liquid, restarting his daily Flovent controller inhaler with a spacer, and keeping the Albuterol rescue inhaler readily accessible.",
            medications: [
              {
                name: "Prednisolone Oral Solution (15 mg / 5 mL)",
                nickname: "Oral corticosteroid",
                timing: "10 mL (30 mg) by mouth once daily with breakfast for 3 days",
                purpose: "Resolves internal airway inflammation and reduces relapse risk.",
                warning: "Administer with food. Complete the 3-day course."
              },
              {
                name: "Fluticasone (Flovent HFA 44 mcg)",
                nickname: "Inhaled maintenance steroid",
                timing: "2 puffs twice daily (morning & night) using AeroChamber spacer",
                purpose: "Daily maintenance to prevent future flare-ups.",
                warning: "Rinse mouth and spit after each use to prevent oral thrush."
              },
              {
                name: "Albuterol HFA (90 mcg)",
                nickname: "Fast-acting bronchodilator",
                timing: "2 puffs with spacer every 4-6 hours as needed for acute symptoms",
                purpose: "Relaxes bronchial smooth muscle during acute bronchospasm.",
                warning: "May cause temporary fast heartbeat or mild hand shakiness."
              }
            ],
            dailyRules: [
              "Always administer inhalers through the spacer holding chamber for optimal lung delivery.",
              "Oral rinse routine: Swish and spit water immediately following Flovent administration.",
              "Follow the Green/Yellow/Red action zone plan posted on your refrigerator."
            ],
            warningSigns: [
              "Subcostal or intercostal retractions (chest or stomach pulling in hard to breathe)",
              "Inability to speak complete sentences without pausing for breath",
              "Peak flow drops below 50% or symptoms worsen despite albuterol",
              "Cyanosis (bluish tint around mouth or nailbeds) - Call 911"
            ],
            followUp: [
              "Pediatric clinic appointment with Dr. Chang within 3 to 5 days"
            ]
          },
          "advanced": {
            overview: "Lucas has reached stable recovery following an acute viral-induced moderate asthma exacerbation. Bronchial hyperreactivity resolved with aerosolized beta-2 agonists and systemic corticosteroids. Post-discharge regimen focuses on finishing the oral steroid burst, resuming anti-inflammatory maintenance therapy, and adhering to strict zone-based asthma triggers.",
            medications: [
              {
                name: "Prednisolone 15mg/5mL oral liquid",
                nickname: "Systemic corticosteroid burst",
                timing: "10 mL (30 mg) PO qAM with food x 3 days",
                purpose: "Suppression of eosinophilic airway inflammatory cascade.",
                warning: "Administer in morning to align with circadian cortisol peaks."
              },
              {
                name: "Fluticasone Propionate (Flovent 44 mcg)",
                nickname: "Inhaled corticosteroid (ICS)",
                timing: "2 actuations BID via valved holding chamber",
                purpose: "Baseline bronchial airway mucosal stabilization.",
                warning: "Mandatory oral rinse and expectoration."
              },
              {
                name: "Albuterol sulfate (ProAir/Ventolin)",
                nickname: "Short-acting beta-2 agonist (SABA)",
                timing: "2 puffs q4-6h PRN bronchospasm via spacer",
                purpose: "Rapid bronchodilation through smooth muscle relaxation.",
                warning: "Escalate to emergency services if refractoriness observed."
              }
            ],
            dailyRules: [
              "Valved holding chamber mechanics: Ensure secure facial seal and 5-6 tidal breaths per puff.",
              "Action zone monitoring: Maintain home peak flow meter log morning and evening.",
              "Viral prophylaxis: Hand hygiene and environmental allergen avoidance."
            ],
            warningSigns: [
              "Increased work of breathing with sternocleidomastoid retractions",
              "Persistent tachypnea > 30 bpm at rest",
              "SABA dependence (> 6 puffs in 24 hours without symptom relief)"
            ],
            followUp: [
              "Pediatric pulmonary assessment with Dr. Chang in 3-5 days"
            ]
          }
        },
        "es": {
          "standard": {
            overview: "Lucas tuvo un ataque de asma provocado por un resfriado viral, lo que le provocó tos y dificultad para respirar. Con los tratamientos en el hospital sus pulmones se despejaron y ya respira normalmente. Siga este plan para continuar cuidándolo en casa.",
            medications: [
              {
                name: "Prednisolona líquida (15 mg / 5 mL)",
                nickname: "Medicamento desinflamatorio líquido",
                timing: "Dar 10 mL (2 cucharaditas) cada mañana con el desayuno por 3 días",
                purpose: "Desinflama los bronquios para evitar que vuelva a toser.",
                warning: "Déselo siempre con comida durante los próximos 3 días."
              },
              {
                name: "Inhalador Flovent (color naranja)",
                nickname: "Inhalador protector diario",
                timing: "2 disparos en la mañana y 2 en la noche con la aerocámara (espaciador)",
                purpose: "Protege sus pulmones a diario para prevenir nuevos ataques.",
                warning: "Haga que se enjuague la boca con agua y la escupa después de usarlo."
              },
              {
                name: "Inhalador Albuterol (color azul)",
                nickname: "Inhalador de rescate rápido",
                timing: "2 disparos con espaciador cada 4 a 6 horas SOLO SI tose o le silba el pecho",
                purpose: "Abre los bronquios rápidamente si tiene problemas para respirar.",
                warning: "Llévelo siempre en su mochila o cuando salgan de casa."
              }
            ],
            dailyRules: [
              "Use siempre la cámara espaciadora transparente con ambos inhaladores.",
              "Enjuáguele la boca con agua después del inhalador naranja.",
              "Tenga el inhalador azul de rescate siempre a la mano."
            ],
            warningSigns: [
              "Respira muy rápido o se le hunden las costillas o el estómago al respirar",
              "No puede hablar oraciones completas por falta de aire",
              "Labios o uñas con tono morado o azulado (LLAME AL 911 DE INMEDIATO)",
              "Tos que no mejora 20 minutos después de usar el inhalador azul"
            ],
            followUp: [
              "Cita con el pediatra Dr. Chang en 3 a 5 días"
            ]
          }
        }
      },

      factualAudit: {
        status: "verified",
        score: "100%",
        summary: "Pediatric steroid liquid duration (3 remaining days), Flovent/Albuterol spacer instructions, rinse-and-spit warnings, and follow-up with Dr. Chang match notes.",
        checks: [
          { item: "Steroid Solution Dosage Match", status: "pass", detail: "Prednisolone 10 mL (30mg) once daily x 3 days strictly verified." },
          { item: "Spacer Delivery Device Safety", status: "pass", detail: "AeroChamber holding chamber specified for both Flovent and Albuterol." },
          { item: "Thrush Prevention Oral Rinse", status: "pass", detail: "Mandatory mouth rinse after inhaled corticosteroid included." },
          { item: "Emergency Red Zone Criteria", status: "pass", detail: "Chest retractions, speech difficulty, and cyanosis highlighted as 911 triggers." }
        ]
      },

      readability: {
        original: {
          gradeLevel: "College Sophomore (Grade 13.8)",
          fleschReadingEase: 32.4,
          jargonDensity: "35.1%",
          avgSentenceLength: "18.5 words",
          tone: "Clinical Pediatric Summary"
        },
        generated: {
          gradeLevel: "4th Grade (Grade 4.8)",
          fleschReadingEase: 91.2,
          jargonDensity: "1.4%",
          avgSentenceLength: "8.2 words",
          tone: "Parent-Friendly, Clear & Caring"
        },
        vocabularyTranslation: [
          { medical: "Acute asthma exacerbation", patient: "Asthma flare-up / attack" },
          { medical: "Intercostal retractions", patient: "Ribs and stomach sucking in hard to breathe" },
          { medical: "AeroChamber valved spacer", patient: "Clear holding tube attached to inhaler" },
          { medical: "Inhaled corticosteroid (ICS)", patient: "Daily protective puffer that calms lung swelling" },
          { medical: "SABA bronchodilator", patient: "Quick-relief rescue puffer" }
        ]
      }
    },

    {
      id: "allergy_conflict_demo",
      title: "⚠️ High-Risk Case: Penicillin Allergy & Medication Discrepancy",
      category: "Patient Safety & Quality Audit",
      tag: "Potential Mismatch",
      patientInfo: {
        name: "David Kowalski",
        age: 62,
        mrn: "MRN-773190",
        admissionDate: "2026-09-22",
        dischargeDate: "2026-09-24",
        attending: "Dr. Sarah Lin, MD"
      },
      originalNote: `DISCHARGE SUMMARY - CAUTION / PENDING RECONCILIATION
PATIENT: Kowalski, David | MRN: 773190 | AGE: 62 | SEX: M
ADMISSION DATE: 09/22/2026 | DISCHARGE DATE: 09/24/2026
ALLERGIES: PENICILLIN (DOCUMENTED SEVERE ANAPHYLAXIS - ANGIOEDEMA & STRIDOR IN 2021)

PRIMARY DIAGNOSIS:
1. Acute uncomplicated bacterial sinusitis with maxillary facial tenderness.
2. Mild tension headaches.

CLINICAL COURSE:
Patient admitted for refractory facial pressure and purulent nasal discharge. CT sinuses showed bilateral maxillary opacification without intracranial extension. Patient afebrile.

DISCHARGE ORDERS (DRAFT):
1. Augmentin (Amoxicillin / Clavulanate) 875/125 mg PO twice daily for 7 days.
2. Fluticasone propionate nasal spray 1 spray per nostril daily.
3. Saline nasal irrigation BID.
4. Follow up in ENT clinic in 10 days.`,
      
      translations: {
        "en": {
          "basic": {
            overview: "⚠️ ATTENTION CLINICIAN & PATIENT: This discharge instruction draft has been flagged for safety review. The hospital notes list an allergy to Penicillin, but an Amoxicillin-type medicine (Augmentin) was drafted. Your medical team must confirm a safe non-penicillin alternative before you leave.",
            medications: [
              {
                name: "⚠️ AUGMENTIN 875/125 mg - [FLAGGED FOR REVIEW]",
                nickname: "POTENTIAL ALLERGY CONFLICT",
                timing: "DO NOT TAKE UNTIL DOCTOR APPROVES",
                purpose: "Antibiotic intended for sinus infection.",
                warning: "CRITICAL: You have a documented severe allergy to Penicillin. Augmentin contains Amoxicillin (a penicillin). An alternative like Doxycycline or Azithromycin should be prescribed."
              },
              {
                name: "Fluticasone Nasal Spray",
                nickname: "Steroid nose spray",
                timing: "1 spray in each nostril every morning",
                purpose: "Reduces swelling in the nose and sinus passages.",
                warning: "Blow nose gently before spraying."
              },
              {
                name: "Saline Nasal Rinse",
                nickname: "Salt water rinse",
                timing: "Rinse sinuses 2 times a day (morning & evening)",
                purpose: "Washes out mucus and keeps nasal passages clean.",
                warning: "Use distilled, sterile, or boiled water only."
              }
            ],
            dailyRules: [
              "Do not take any antibiotic until your physician verifies a non-penicillin alternative.",
              "Rinse nasal passages gently with clean saline rinse twice daily.",
              "Drink plenty of water and rest with your head slightly elevated."
            ],
            warningSigns: [
              "Swelling of the lips, tongue, or throat (CALL 911 IMMEDIATELY)",
              "Difficulty breathing or wheezing",
              "Severe facial pain spreading to the eye or forehead",
              "High fever above 101.5°F"
            ],
            followUp: [
              "ENT Specialist Clinic in 10 days",
              "Immediate doctor review of antibiotic before hospital discharge"
            ]
          },
          "standard": {
            overview: "⚠️ CLINICAL SAFETY HOLD: The discharge summary generated an alert. The clinical record indicates a documented severe anaphylactic allergy to Penicillin. However, the draft medication list includes Augmentin (Amoxicillin/Clavulanate), which is a penicillin-class antibiotic with direct cross-reactivity. A clinician must reconcile and approve an alternative regimen (such as Doxycycline or Levofloxacin).",
            medications: [
              {
                name: "⚠️ Augmentin 875/125 mg [BLOCKED - ALLERGY CONFLICT]",
                nickname: "Contraindicated Penicillin Antibiotic",
                timing: "HOLD - Awaiting Physician Override or Substitution",
                purpose: "Intended for acute bacterial sinusitis.",
                warning: "SEVERE WARNING: Patient has documented anaphylaxis to penicillin class. High risk of life-threatening allergic reaction."
              },
              {
                name: "Fluticasone Propionate Nasal Spray",
                nickname: "Topical nasal corticosteroid",
                timing: "1 spray in each nostril once daily",
                purpose: "Reduces nasal mucosal inflammation and promotes sinus drainage.",
                warning: "Aim spray away from nasal septum."
              },
              {
                name: "Sinus Saline Rinse",
                nickname: "Nasal lavage",
                timing: "Twice daily morning and evening",
                purpose: "Clears purulent secretions from nasal cavity.",
                warning: "Always use sterile or distilled water."
              }
            ],
            dailyRules: [
              "Medication Safety Hold: Do not dispense or ingest penicillin derivatives.",
              "Sinus Hygiene: Perform saline irrigation twice daily; avoid forceful nose blowing.",
              "Hydration: Maintain oral hydration to thin mucus secretions."
            ],
            warningSigns: [
              "Anaphylaxis symptoms: facial/lip angioedema, throat tightness, stridor, urticaria (CALL 911)",
              "Periorbital swelling, double vision, or visual changes",
              "Severe stiff neck with high fever"
            ],
            followUp: [
              "ENT Clinic evaluation in 10 days",
              "Pharmacy reconciliation prior to discharge"
            ]
          },
          "advanced": {
            overview: "SAFETY ALERT: Incongruity identified between recorded patient allergy profile (Penicillin - anaphylaxis/angioedema) and proposed antimicrobial therapy (Augmentin / Amoxicillin-clavulanate). Beta-lactam cross-reactivity is 100%. Clinician intervention mandatory to switch to non-beta-lactam alternative (e.g., Doxycycline 100mg PO BID or Respiratory Fluoroquinolone).",
            medications: [
              {
                name: "⚠️ Augmentin (Amoxicillin/Clavulanate) 875/125 mg PO BID",
                nickname: "SAFETY INTERCEPTION",
                timing: "BLOCKED",
                purpose: "Empiric sinusitis coverage.",
                warning: "Contraindicated secondary to documented IgE-mediated anaphylaxis to aminopenicillins."
              },
              {
                name: "Fluticasone Propionate 50 mcg/actuation",
                nickname: "Intranasal corticosteroid",
                timing: "1 spray/nostril daily",
                purpose: "Decongestion and osteomeatal complex drainage.",
                warning: "Ensure lateral orientation."
              },
              {
                name: "Nasal Saline Lavage",
                nickname: "Hypertonic/isotonic lavage",
                timing: "BID PRN",
                purpose: "Mucociliary clearance enhancement.",
                warning: "Strict adherence to sterile fluid reconstitution."
              }
            ],
            dailyRules: [
              "Immediate Allergy Override Required: Pharmacy hold active.",
              "Sinusitis self-care: Warm compresses, humidified air.",
              "Vigilant monitoring for orbital or meningeal extension."
            ],
            warningSigns: [
              "Anaphylactoid symptoms",
              "Preseptal or orbital cellulitis signs",
              "Meningismus or persistent neurologic deficits"
            ],
            followUp: [
              "Otolaryngology clinic in 10 days"
            ]
          }
        },
        "es": {
          "standard": {
            overview: "⚠️ ALERTA DE SEGURIDAD CLÍNICA: Se ha retenido el borrador de instrucciones de alta. El historial médico indica una alergia anafiláctica grave a la Penicilina. Sin embargo, la lista de medicamentos incluye Augmentin (Amoxicilina/Clavulanato), que es un antibiótico derivado de la penicilina con riesgo de reacción cruzada grave. El médico debe confirmar una alternativa segura antes del alta.",
            medications: [
              {
                name: "⚠️ Augmentin 875/125 mg [BLOQUEADO - CONFLICTO DE ALERGIA]",
                nickname: "Antibiótico contraindicado",
                timing: "NO TOMAR - Esperando cambio de receta del médico",
                purpose: "Antibiótico destinado a la infección de senos nasales.",
                warning: "PELIGRO: El paciente tiene alergia grave documentada a la penicilina. Riesgo de reacción alérgica potencialmente mortal."
              },
              {
                name: "Fluticasona Spray Nasal",
                nickname: "Spray nasal antiinflamatorio",
                timing: "1 aplicación en cada fosa nasal una vez al día",
                purpose: "Desinflama los conductos nasales y facilita la ventilación.",
                warning: "Sonarse suavemente antes de aplicar."
              },
              {
                name: "Lavado Nasal Salino",
                nickname: "Lavado con solución salina",
                timing: "Dos veces al día (mañana y noche)",
                purpose: "Limpia las secreciones de los senos nasales.",
                warning: "Usar siempre agua destilada o hervida."
              }
            ],
            dailyRules: [
              "Retención de medicación: No tomar penicilina ni derivados bajo ninguna circunstancia.",
              "Lavados nasales dos veces al día con suavidad.",
              "Mantener buena hidratación para disolver la mucosidad."
            ],
            warningSigns: [
              "Hinchazón en labios, lengua o garganta (LLAMAR AL 911 DE INMEDIATO)",
              "Dificultad para respirar o pitos en el pecho",
              "Fiebre alta superior a 38.5°C o rigidez en el cuello"
            ],
            followUp: [
              "Cita en la clínica de Otorrinolaringología (ENT) en 10 días",
              "Aprobación obligatoria de nuevo antibiótico por el médico antes de salir"
            ]
          }
        }
      },

      factualAudit: {
        status: "mismatch", // Mismatch state!
        score: "⚠️ 62% - Action Required",
        summary: "CRITICAL SAFETY MISMATCH: Documented severe penicillin allergy contradicts draft prescription for Augmentin (Amoxicillin/Clavulanate). Automatic safety hold activated!",
        checks: [
          { item: "Cross-Reactivity Allergy Check", status: "fail", detail: "Documented Penicillin anaphylaxis (2021) conflicts directly with Augmentin (contains amoxicillin)." },
          { item: "Medication Reconciliation", status: "warning", detail: "Augmentin flagged. Recommended substitute: Doxycycline 100mg BID x7d or Cefuroxime (if cephalosporin tolerated) or Azithromycin." },
          { item: "Nasal Therapy Verification", status: "pass", detail: "Fluticasone nasal spray and saline rinses verified safe." },
          { item: "Follow-up Timeline Check", status: "pass", detail: "ENT clinic visit in 10 days matched." }
        ]
      },

      readability: {
        original: {
          gradeLevel: "College Junior (Grade 14.1)",
          fleschReadingEase: 30.1,
          jargonDensity: "36.8%",
          avgSentenceLength: "17.4 words",
          tone: "Hospital Progress Note"
        },
        generated: {
          gradeLevel: "5th Grade (Grade 5.6)",
          fleschReadingEase: 87.2,
          jargonDensity: "2.4%",
          avgSentenceLength: "9.5 words",
          tone: "High-Alert Safety Guidance"
        },
        vocabularyTranslation: [
          { medical: "Documented anaphylaxis", patient: "Severe, life-threatening allergic reaction" },
          { medical: "Bacterial sinusitis", patient: "Sinus infection causing facial pressure and stuffiness" },
          { medical: "Purulent nasal discharge", patient: "Thick yellow or green nasal mucus" },
          { medical: "Intranasal corticosteroid", patient: "Gentle anti-swelling nose spray" },
          { medical: "Maxillary opacification", patient: "Cloudy, blocked sinus pockets shown on scan" }
        ]
      }
    }
  ],

  // Translation languages available in dropdown
  languages: [
    { code: "en", name: "English", flag: "🇺🇸", nativeName: "English" },
    { code: "es", name: "Spanish", flag: "🇪🇸", nativeName: "Español" },
    { code: "zh", name: "Chinese (Simplified)", flag: "🇨🇳", nativeName: "简体中文" },
    { code: "vi", name: "Vietnamese", flag: "🇻🇳", nativeName: "Tiếng Việt" },
    { code: "tl", name: "Tagalog", flag: "🇵🇭", nativeName: "Tagalog" },
    { code: "ar", name: "Arabic", flag: "🇸🇦", nativeName: "العربية" },
    { code: "fr", name: "French", flag: "🇫🇷", nativeName: "Français" },
    { code: "hi", name: "Hindi", flag: "🇮🇳", nativeName: "हिन्दी" },
    { code: "ta", name: "Tamil", flag: "🇮🇳", nativeName: "தமிழ்" }
  ],

  // Synthetic Patient Presets (Requirement 1 & 10: Dynamic Cases)
  patientPresets: {
    "maria_gonzalez": {
      patient_name: "Maria Gonzalez",
      patient_id: "MRN-501928",
      age: 62,
      gender: "Female",
      doctor_name: "Dr. Carlos Ramirez, MD",
      clinic_name: "San Gabriel Endocrine & Wound Clinic",
      diagnosis: "Type 2 Diabetes Mellitus & Lower Extremity Wound",
      symptoms: "Erythema and edema in right heel, peripheral tingling, fasting glucose 195 mg/dL",
      medical_history: "Type 2 Diabetes (12 yrs), Diabetic Retinopathy, Hypertension",
      allergies: "Sulfa drugs (rash / hives)",
      current_medications: "Metformin 500mg BID with meals, Lisinopril 20mg daily",
      treatment_instructions: "Clean wound once daily with sterile saline, apply dry sterile gauze. Avoid barefoot walking. Inspect both feet every evening.",
      follow_up_date: "Wound Care Clinic in 7 days (Oct 3 at 9:00 AM)",
      clinical_notes: "Patient educated on diabetic foot care rules, daily blood glucose monitoring, and signs of systemic infection.",
      rx_sample: "diabetes"
    },
    "david_chen": {
      patient_name: "David Chen",
      patient_id: "MRN-618402",
      age: 45,
      gender: "Male",
      doctor_name: "Dr. Angela Patel, MD",
      clinic_name: "Valley Pulmonary & Urgent Care",
      diagnosis: "Acute Bronchitis & Stage 1 Hypertension",
      symptoms: "Productive cough for 6 days, mild wheezing on expiration, BP 142/88 mmHg",
      medical_history: "Mild seasonal allergies, essential hypertension",
      allergies: "No known drug allergies (NKDA)",
      current_medications: "Amlodipine 5mg daily in morning",
      treatment_instructions: "Increase warm oral hydration (8-10 glasses/day). Rest for 48-72 hours. Avoid secondhand smoke and cold air.",
      follow_up_date: "Follow up with primary care physician in 2 weeks if cough persists",
      clinical_notes: "Patient educated on correct inhaler technique with spacer and swallowing Tessalon perles whole without biting.",
      rx_sample: "bronchitis"
    },
    "robert_hernandez": {
      patient_name: "Robert Hernandez",
      patient_id: "MRN-849201",
      age: 68,
      gender: "Male",
      doctor_name: "Dr. Sarah Lin, MD",
      clinic_name: "Metropolitan Cardiology Institute",
      diagnosis: "Acute Decompensated Heart Failure (HFrEF)",
      symptoms: "Dyspnea on exertion, orthopnea (3 pillows), bilateral pitting pedal edema",
      medical_history: "Coronary artery disease, HFrEF (EF 32%), Chronic hypertension",
      allergies: "No known drug allergies (NKDA)",
      current_medications: "Furosemide 40mg PO qAM, Carvedilol 6.25mg BID, Lisinopril 10mg daily",
      treatment_instructions: "Strict sodium limit < 2,000 mg/day. Fluid restriction 1,500 mL/day. Weigh self every morning after voiding.",
      follow_up_date: "Heart Failure Clinic in 10 days with repeat Basic Metabolic Panel",
      clinical_notes: "Euvolemic at discharge. Warned against fluid overload and sudden weight gain.",
      rx_sample: "cardio"
    },
    "liam_bennett": {
      patient_name: "Liam Bennett",
      patient_id: "MRN-712034",
      age: 7,
      gender: "Male",
      doctor_name: "Dr. Marcus Vance, MD",
      clinic_name: "Children's Health Pavilion",
      diagnosis: "Pediatric Asthma Exacerbation",
      symptoms: "Expiratory wheezing, nighttime coughing, respiratory rate 26/min",
      medical_history: "Childhood asthma, eczema, allergic rhinitis",
      allergies: "No known drug allergies (NKDA)",
      current_medications: "Flovent HFA 44mcg 2 puffs BID with spacer",
      treatment_instructions: "Always use clear AeroChamber spacer with puffers. Rinse and spit water after controller inhaler. Avoid cold air.",
      follow_up_date: "Pediatrician check-up in 3 to 5 days",
      clinical_notes: "Caregiver demonstrated correct spacer seal. Green/Yellow/Red action plan reviewed.",
      rx_sample: "asthma"
    },
    "emily_kowalski": {
      patient_name: "Emily Kowalski",
      patient_id: "MRN-394821",
      age: 34,
      gender: "Female",
      doctor_name: "Dr. Kevin Ross, MD",
      clinic_name: "Eastside Sinus & Allergy Center",
      diagnosis: "Acute Bacterial Sinusitis",
      symptoms: "Facial pain and pressure, nasal purulence for 10 days, frontal headache",
      medical_history: "Recurrent rhinosinusitis, environmental allergies",
      allergies: "Penicillin (Severe Anaphylaxis / Throat Swelling)",
      current_medications: "Fluticasone propionate nasal spray 1 spray daily",
      treatment_instructions: "Saline nasal irrigation BID. Hold any penicillin-class antibiotic (Augmentin) pending allergy reconciliation.",
      follow_up_date: "ENT clinic follow-up in 10 days",
      clinical_notes: "SAFETY ALERT: Prescribed Augmentin must be stopped due to severe penicillin anaphylaxis.",
      rx_sample: "allergy_demo"
    }
  },

  // Prescription Sample Templates (Requirement 2 & 3)
  prescriptionPresets: {
    "diabetes": {
      filename: "rx_wound_care_mg.pdf",
      extracted: {
        medicines: [
          { name: "Cephalexin (Keflex)", dosage: "500 mg", frequency: "4 times daily (every 6 hours)", duration: "10 days", instructions: "Complete entire 10-day course even if wound looks healed" }
        ],
        doctor_instructions: "Clean right heel wound once daily with sterile saline. Keep dressing clean and dry. Never walk barefoot.",
        follow_up: "Wound Care Clinic follow-up in 7 days (Oct 3 at 9:00 AM)",
        doctor_name: "Dr. Carlos Ramirez, MD",
        clinic_name: "San Gabriel Endocrine & Wound Clinic"
      }
    },
    "bronchitis": {
      filename: "rx_bronchitis_dc.png",
      extracted: {
        medicines: [
          { name: "Albuterol HFA Inhaler", dosage: "90 mcg (2 puffs)", frequency: "Every 4 to 6 hours as needed", duration: "PRN (as needed)", instructions: "Inhale 2 puffs for wheezing or chest tightness. Rinse mouth after use." },
          { name: "Benzonatate (Tessalon Perles)", dosage: "100 mg", frequency: "3 times daily as needed for cough", duration: "5 days", instructions: "Swallow whole with water; do not bite, chew, or crush capsule." }
        ],
        doctor_instructions: "Drink 8 to 10 glasses of warm water or tea daily. Rest and avoid tobacco smoke.",
        follow_up: "Check with primary doctor in 2 weeks if cough persists",
        doctor_name: "Dr. Angela Patel, MD",
        clinic_name: "Valley Pulmonary & Urgent Care"
      }
    },
    "cardio": {
      filename: "rx_cardiology_rh.pdf",
      extracted: {
        medicines: [
          { name: "Furosemide (Lasix)", dosage: "40 mg", frequency: "Once daily at 8:00 AM", duration: "30 days", instructions: "Take in the morning with a full glass of water. Avoid evening doses." },
          { name: "Carvedilol (Coreg)", dosage: "6.25 mg", frequency: "Twice daily with meals (morning and evening)", duration: "30 days", instructions: "Take with breakfast and dinner." }
        ],
        doctor_instructions: "Daily morning weigh-in post-voiding. Fluid limit 1,500 mL/day. Dietary sodium < 2,000 mg/day.",
        follow_up: "Heart Failure Clinic in 10 days with repeat BMP lab panel",
        doctor_name: "Dr. Sarah Lin, MD",
        clinic_name: "Metropolitan Cardiology Institute"
      }
    },
    "asthma": {
      filename: "rx_pediatric_asthma_lb.png",
      extracted: {
        medicines: [
          { name: "Flovent HFA (Fluticasone)", dosage: "44 mcg (2 puffs)", frequency: "Twice daily (morning and evening)", duration: "Ongoing controller", instructions: "Always use with AeroChamber spacer. Rinse and spit water after use." },
          { name: "Albuterol Inhaler (Ventolin)", dosage: "90 mcg (2 puffs)", frequency: "Every 4 hours as needed for coughing or wheezing", duration: "PRN (rescue)", instructions: "Quick-relief rescue inhaler. Keep accessible at all times." },
          { name: "Prednisolone Oral Liquid", dosage: "15 mg/5 mL (10 mL)", frequency: "Once daily in the morning with food", duration: "3 days", instructions: "Complete full 3-day course with breakfast." }
        ],
        doctor_instructions: "Avoid cold dry air and pet dander. Follow green/yellow/red action plan.",
        follow_up: "Pediatrician check-up in 3 to 5 days",
        doctor_name: "Dr. Marcus Vance, MD",
        clinic_name: "Children's Health Pavilion"
      }
    },
    "allergy_demo": {
      filename: "rx_allergy_conflict_ek.pdf",
      extracted: {
        medicines: [
          { name: "Augmentin (Amoxicillin/Clavulanate)", dosage: "875/125 mg", frequency: "Twice daily with meals", duration: "7 days", instructions: "⚠️ CAUTION: Beta-lactam antibiotic. Severe cross-reactivity with Penicillin allergy!" },
          { name: "Fluticasone Propionate Nasal Spray", dosage: "50 mcg", frequency: "1 spray in each nostril once daily", duration: "14 days", instructions: "Blow nose gently before administering." }
        ],
        doctor_instructions: "Perform gentle saline nasal rinses twice daily. Report rash, facial swelling, or breathing difficulty immediately.",
        follow_up: "ENT Clinic follow-up in 10 days",
        doctor_name: "Dr. Kevin Ross, MD",
        clinic_name: "Eastside Sinus & Allergy Center"
      }
    }
  },

  // Literacy levels available
  literacyLevels: [
    {
      id: "basic",
      label: "Basic (5th Grade)",
      badge: "Grade 4-5",
      description: "Simple conversational words, clear analogies, short sentences. Ideal for low-health-literacy patients.",
      icon: "book-open"
    },
    {
      id: "standard",
      label: "Standard (8th Grade)",
      badge: "Grade 7-8 • Recommended",
      description: "Balanced, patient-friendly medical explanations with actionable schedules and warning signs.",
      icon: "check-circle",
      isDefault: true
    },
    {
      id: "advanced",
      label: "Advanced (Caregiver / High School)",
      badge: "Grade 10-12",
      description: "Detailed clinical rationale and structured monitoring protocol for experienced family caregivers.",
      icon: "graduation-cap"
    }
  ]
};

// Export to window for browser access
if (typeof window !== "undefined") {
  window.MOCK_DATA = MOCK_DATA;
}

