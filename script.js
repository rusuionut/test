const questions = [
    // --- CAPITOLUL 1: Examen psihic & Semiologie (35 intrebari) ---
    {
        question: "1. Hiperestezia senzorială reprezintă:",
        options: [
            { text: "Ridicarea pragului senzorial", feedback: "Incorect. Aceasta se numește hipoestezie." },
            { text: "Scăderea pragului senzorial cu creșterea sensibilității", feedback: "Corect. Hiperestezia înseamnă sensibilitate crescută la stimuli (zgomote, lumini)." },
            { text: "Percepție fără obiect", feedback: "Incorect. Aceasta este halucinația." }
        ],
        correctIndex: 1
    },
    {
        question: "2. Iluziile fiziologice:",
        options: [
            { text: "Apar doar în schizofrenie", feedback: "Incorect. Acelea sunt iluzii patologice." },
            { text: "Sunt corectate de subiect (își dă seama de eroare)", feedback: "Corect. Iluziile fiziologice apar la oameni normali (ex: distanță, întuneric) și sunt criticate." },
            { text: "Sunt convingeri false", feedback: "Incorect. Iluziile sunt tulburări de percepție, nu de gândire." }
        ],
        correctIndex: 1
    },
    {
        question: "3. Metamorfopsiile sunt iluzii vizuale care constau în:",
        options: [
            { text: "Impresia de deformare a obiectelor/spațiului", feedback: "Corect. Obiectele sunt percepute deformat." },
            { text: "Perceperea obiectelor mult mai mici (liliputane)", feedback: "Incorect. Aceasta se numește micropsie (deși e un tip de metamorfopsie, definiția generală e deformarea)." },
            { text: "Perceperea obiectelor infrumusețate", feedback: "Incorect. Aceasta este callopsia." }
        ],
        correctIndex: 0
    },
    {
        question: "4. Halucinațiile propriu-zise (psihosenzoriale) se caracterizează prin:",
        options: [
            { text: "Lipsa proiecției spațiale", feedback: "Incorect. Acelea sunt pseudohalucinații." },
            { text: "Proiecție spațială și convingerea realității lor", feedback: "Corect. Sunt percepute în exterior și considerate reale de pacient." },
            { text: "Recunoașterea caracterului patologic", feedback: "Incorect. Acelea sunt halucinoze." }
        ],
        correctIndex: 1
    },
    {
        question: "5. Pseudohalucinațiile sunt percepute de pacient:",
        options: [
            { text: "În spațiul extern (extracampin)", feedback: "Incorect. Acelea sunt halucinații propriu-zise." },
            { text: "În mintea sa ('văd cu ochii minții')", feedback: "Corect. Nu au senzorialitate și par impuse din exterior în minte." },
            { text: "Doar la adormire", feedback: "Incorect. Acelea sunt halucinații hipnagogice." }
        ],
        correctIndex: 1
    },
    {
        question: "6. Hiperprosexia (creșterea concentrării atenției) apare în:",
        options: [
            { text: "Stările confuzionale", feedback: "Incorect. Acolo apare hipoprosexia/aprosexia." },
            { text: "Oligofrenie", feedback: "Incorect. Oligofrenia se asociază cu hipoprosexie." },
            { text: "Episoade expansive, hipocondrie, obsesii", feedback: "Corect. Atenția este exagerat orientată selectiv (ex: spre simptome în hipocondrie)." }
        ],
        correctIndex: 2
    },
    {
        question: "7. Criptomnezia este o tulburare de memorie în care:",
        options: [
            { text: "Pacientul uită tot trecutul", feedback: "Incorect. Aceasta e amnezie retrogradă." },
            { text: "O lucrare străină este considerată proprie (plagiat involuntar)", feedback: "Corect. Pacientul crede că el a creat ceva ce de fapt a văzut/auzit anterior." },
            { text: "Persoanele necunoscute par cunoscute", feedback: "Incorect. Aceasta este falsă recunoaștere." }
        ],
        correctIndex: 1
    },
    {
        question: "8. Confabulațiile reprezintă:",
        options: [
            { text: "Relatarea unor evenimente imaginare crezute ca reale (umplerea golurilor)", feedback: "Corect. Pacientul 'inventează' inconștient pentru a acoperi lacunele mnezice (ex: Korsakov)." },
            { text: "Minciuna intenționată", feedback: "Incorect. Confabulația nu este intenționată." },
            { text: "Retrăirea trecutului ca prezent", feedback: "Incorect. Aceasta este ecmnezia." }
        ],
        correctIndex: 0
    },
    {
        question: "9. Obtuzia este o tulburare cantitativă a conștiinței caracterizată prin:",
        options: [
            { text: "Pierderea completă a conștiinței (comă)", feedback: "Incorect." },
            { text: "Imprecizie și dificultăți asociative (forma ușoară)", feedback: "Corect. Este o reducere ușoară a clarității conștiinței." },
            { text: "Dezorientare totală și halucinații terifiante", feedback: "Incorect. Acesta este delirium (confuzia mintală)." }
        ],
        correctIndex: 1
    },
    {
        question: "10. 'Salata de cuvinte' reprezintă:",
        options: [
            { text: "Accelerarea ritmului vorbirii", feedback: "Incorect. Aceasta este logoree/tahifemie." },
            { text: "Amestec de cuvinte fără legătură logică (incoerență maximă)", feedback: "Corect. Apare în schizofrenie și demențe grave." },
            { text: "Repetarea stereotipă a unui cuvânt", feedback: "Incorect. Aceasta este stereotipie verbală sau verbigerație." }
        ],
        correctIndex: 1
    },
    {
        question: "11. Fuga de idei se asociază frecvent cu:",
        options: [
            { text: "Bradipsihia (gândire lentă)", feedback: "Incorect." },
            { text: "Tahipsihia (accelerarea ritmului ideativ)", feedback: "Corect. Ideile se succed rapid, superficial (asociații prin rimă/asonanță), tipic în manie." },
            { text: "Barajul ideativ", feedback: "Incorect. Barajul (oprirea gândirii) e specific schizofreniei." }
        ],
        correctIndex: 1
    },
    {
        question: "12. Ideile delirante de referință constau în:",
        options: [
            { text: "Convingerea că pacientul este o persoană importantă", feedback: "Incorect. Acesta este delir de grandoare." },
            { text: "Convingerea că gesturile/cuvintele altora i se adresează lui", feedback: "Corect. Pacientul crede că TV-ul vorbește despre el sau oamenii pe stradă îi fac semne." },
            { text: "Convingerea că este urmărit de poliție", feedback: "Incorect. Acesta este delir de persecuție." }
        ],
        correctIndex: 1
    },
    {
        question: "13. Barajul ideativ (oprirea bruscă a fluxului gândirii) este sugestiv pentru:",
        options: [
            { text: "Episodul maniacal", feedback: "Incorect. Aici apare fuga de idei." },
            { text: "Schizofrenie", feedback: "Corect. Este un simptom clasic de dezorganizare a gândirii în schizofrenie." },
            { text: "Depresie", feedback: "Incorect. Aici apare bradipsihia (încetinirea)." }
        ],
        correctIndex: 1
    },
    {
        question: "14. Paratimiile (inversiunea afectivă, ambivalența) sunt:",
        options: [
            { text: "Tulburări cantitative ale afectivității", feedback: "Incorect. Cantitative sunt hipertimia/hipotimia." },
            { text: "Tulburări calitative (reacții inadecvate)", feedback: "Corect. Emoțiile sunt paradoxale sau neconforme cu situația." },
            { text: "Specifice nevrozelor", feedback: "Incorect. Sunt specifice psihozelor (schizofrenie)." }
        ],
        correctIndex: 1
    },
    {
        question: "15. Disforia se definește ca:",
        options: [
            { text: "O stare de intensă fericire", feedback: "Incorect. Aceasta este euforia." },
            { text: "Stare mixtă: dispoziție depresiv-anxioasă cu iritabilitate", feedback: "Corect. Pacientul este morocănos, irascibil, 'supărat pe lume'." },
            { text: "Lipsă totală de afectivitate", feedback: "Incorect. Aceasta este apatia/atimia." }
        ],
        correctIndex: 1
    },
    {
        question: "16. Abulia reprezintă:",
        options: [
            { text: "Lipsa de inițiativă și incapacitatea de a acționa", feedback: "Corect. Este forma severă a hipobuliei (lipsă voință)." },
            { text: "Exagerarea voinței", feedback: "Incorect. Aceasta este hiperbulie." },
            { text: "Impulsivitate extremă", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "17. Ecopraxia este:",
        options: [
            { text: "Repetarea cuvintelor interlocutorului", feedback: "Incorect. Aceasta este ecolalia." },
            { text: "Imitarea gesturilor interlocutorului", feedback: "Corect. Apare în catatonie/schizofrenie." },
            { text: "Menținerea unei poziții incomode", feedback: "Incorect. Aceasta este catalepsia/flexibilitatea ceroasă." }
        ],
        correctIndex: 1
    },
    {
        question: "18. Negativismul (ca tulburare de activitate) înseamnă:",
        options: [
            { text: "Refuzul sau execuția contrară a unei solicitări", feedback: "Corect. Poate fi pasiv (nu face) sau activ (face invers)." },
            { text: "Pesimism în gândire", feedback: "Incorect. Se referă la activitatea motorie în context semiologic." },
            { text: "Lipsa criticii bolii", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "19. Anxietatea diferă de frică prin faptul că:",
        options: [
            { text: "Este mai intensă", feedback: "Incorect. Frica poate fi foarte intensă." },
            { text: "Nu are obiect precis (teamă difuză)", feedback: "Corect. Frica are un obiect clar, anxietatea este o teamă 'fără obiect'." },
            { text: "Apare doar la copii", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "20. Agitația psihomotorie în manie este:",
        options: [
            { text: "Dezordonată, fără scop și ineficientă", feedback: "Incorect. Aceasta e mai tipică schizofreniei sau confuziei. Mania are o 'polipragmazie' (multe activități începute). Totuși, în manie severă (fureur) poate fi dezordonată. Dar definiția 'fără scop' e mai mult pentru catatonie." },
            { text: "Crescută, dar instabilă (polipragmazie)", feedback: "Corect. Maniacul începe multe, nu termină nimic, e hiperactiv." },
            { text: "Inhibată complet", feedback: "Incorect" }
        ],
        correctIndex: 1
    },
    // --- CAPITOLUL 2: Nevroza vs Psihoza & Scale (15 intrebari) ---
    {
        question: "21. Elementul definitoriu care diferențiază psihoza de nevroză este:",
        options: [
            { text: "Gravitatea simptomelor", feedback: "Incorect. O nevroză poate fi foarte gravă." },
            { text: "Pierderea contactului cu realitatea și lipsa conștiinței bolii", feedback: "Corect. Psihoticul își construiește o realitate proprie (delir) și nu se consideră bolnav." },
            { text: "Prezența anxietății", feedback: "Incorect. Anxietatea apare în ambele." }
        ],
        correctIndex: 1
    },
    {
        question: "22. Nevrozele sunt considerate afecțiuni:",
        options: [
            { text: "Endogene (cauze biologice interne)", feedback: "Incorect. Psihozele sunt adesea endogene." },
            { text: "Exogene (cauzate de psihotraume/stres)", feedback: "Corect. Nevrozele sunt reacții la conflicte/stres." },
            { text: "Incurabile", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "23. Scala BPRS (Brief Psychiatric Rating Scale) măsoară preponderent:",
        options: [
            { text: "Nivelul de inteligență", feedback: "Incorect." },
            { text: "Severitatea simptomelor psihotice", feedback: "Corect. Este standard pentru schizofrenie/psihoze." },
            { text: "Trăsăturile de personalitate", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "24. Scala GAF (Global Assessment of Functioning) evaluează:",
        options: [
            { text: "Doar simptomele depresive", feedback: "Incorect." },
            { text: "Funcționarea psihologică, socială și ocupațională", feedback: "Corect. Un scor 100 înseamnă funcționare excelentă." },
            { text: "Riscul de suicid specific", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "25. Modelul cognitiv al psihozelor susține că delirul apare prin:",
        options: [
            { text: "Exces de dopamină (fără legătură cu gândirea)", feedback: "Incorect. Aceasta e teoria biologică." },
            { text: "Interpretarea eronată a unor intruziuni (halucinații/gânduri)", feedback: "Corect. Pacientul încearcă să explice logic experiențele ciudate (ex: aud voci -> sunt spionat)." },
            { text: "Traume din copilărie exclusiv", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "26. SCL-90 (Symptom Checklist-90) este:",
        options: [
            { text: "Un test de inteligență", feedback: "Incorect." },
            { text: "Un instrument de screening multidimensional", feedback: "Corect. Evaluează 9 dimensiuni (depresie, anxietate, somatizare etc.)." },
            { text: "O tehnică proiectivă", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "27. În nevroză, pacientul:",
        options: [
            { text: "Are conștiința bolii (insight)", feedback: "Corect. Cere ajutor, știe că suferă." },
            { text: "Refuză tratamentul negând boala", feedback: "Incorect. Asta e specific psihozei." },
            { text: "Prezintă halucinații complexe", feedback: "Incorect. Nevroticul rămâne ancorat în realitate." }
        ],
        correctIndex: 0
    },
    {
        question: "28. Un scor mare la scala BPRS indică:",
        options: [
            { text: "O sănătate mintală bună", feedback: "Incorect." },
            { text: "Severitate crescută a psihozei", feedback: "Corect." },
            { text: "Nivel ridicat de IQ", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    // --- CAPITOLUL 3: Schizofrenie & Tulburari psihotice (20 intrebari) ---
    {
        question: "29. Pentru diagnosticul de schizofrenie (DSM-5), simptomele trebuie să persiste cel puțin:",
        options: [
            { text: "1 lună", feedback: "Incorect. 1 lună este pentru tulburarea schizofreniformă (faza activă)." },
            { text: "6 luni", feedback: "Corect. Durata totală (prodromal + activ + rezidual) trebuie să fie > 6 luni." },
            { text: "2 ani", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "30. Care dintre următoarele este un simptom POZITIV în schizofrenie?",
        options: [
            { text: "Alogia", feedback: "Incorect. Este simptom negativ." },
            { text: "Avolitia", feedback: "Incorect. Este simptom negativ." },
            { text: "Ideea delirantă", feedback: "Corect. Simptomele pozitive sunt 'în plus' față de funcționarea normală (delir, halucinații)." }
        ],
        correctIndex: 2
    },
    {
        question: "31. Aplatizarea afectivă (tocirea) înseamnă:",
        options: [
            { text: "Diminuarea expresivității emoționale", feedback: "Corect. Față imobilă, voce monotonă (simptom negativ)." },
            { text: "Tristețe profundă", feedback: "Incorect. Aceasta e depresie." },
            { text: "Schimbări rapide de dispoziție", feedback: "Incorect. Aceasta e labilitate." }
        ],
        correctIndex: 0
    },
    {
        question: "32. Tulburarea delirantă se caracterizează prin:",
        options: [
            { text: "Deliruri bizare, imposibile", feedback: "Incorect. Acelea sunt tipice schizofreniei." },
            { text: "Deliruri non-bizare, plauzibile (ex: gelozie, urmărire)", feedback: "Corect. Temele sunt din viața reală, dar convingerea e falsă/rigidă." },
            { text: "Prezența halucinațiilor vizuale intense", feedback: "Incorect. Halucinațiile sunt rare sau absente în tulburarea delirantă." }
        ],
        correctIndex: 1
    },
    {
        question: "33. Tulburarea schizoafectivă presupune:",
        options: [
            { text: "Doar simptome de schizofrenie", feedback: "Incorect." },
            { text: "Simptome de schizofrenie + Episod major de dispoziție (Depresie/Manie)", feedback: "Corect. Există o perioadă cu simptome psihotice FĂRĂ simptome afective, dar și perioade combinate." },
            { text: "Doar oscilații ale dispoziției", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "34. Delirul de referință presupune:",
        options: [
            { text: "Convingerea că partenerul este infidel", feedback: "Incorect. Acesta e delir de gelozie." },
            { text: "Ideea că evenimente neutre au semnificație specială pentru subiect", feedback: "Corect. Ex: crainicul TV transmite mesaje pentru el." },
            { text: "Ideea că i s-au furat gândurile", feedback: "Incorect. Acesta e delir de furt al gândirii." }
        ],
        correctIndex: 1
    },
    {
        question: "35. Tulburarea psihotică scurtă are o durată de:",
        options: [
            { text: "Mai puțin de 1 zi", feedback: "Incorect." },
            { text: "Între 1 zi și 1 lună", feedback: "Corect. Se remite complet într-o lună." },
            { text: "Între 1 lună și 6 luni", feedback: "Incorect. Aceasta e tulburarea schizofreniformă." }
        ],
        correctIndex: 1
    },
    {
        question: "36. Psihoza postpartum:",
        options: [
            { text: "Este o ușoară tristețe după naștere", feedback: "Incorect. Aceasta e 'baby blues'." },
            { text: "Este o urgență psihiatrică cu risc de infanticid", feedback: "Corect. Mama are delir/halucinații și poate face rău copilului." },
            { text: "Trece de la sine fără tratament", feedback: "Incorect. Necesită internare/tratament." }
        ],
        correctIndex: 1
    },
    {
        question: "37. Care NU este un subtip de idee delirantă?",
        options: [
            { text: "Erotoman", feedback: "Incorect. (Este subtip)." },
            { text: "Catatonic", feedback: "Corect. Catatonia este o tulburare psihomotorie, nu un tip de delir." },
            { text: "Somatic", feedback: "Incorect. (Este subtip)." }
        ],
        correctIndex: 1
    },
    {
        question: "38. Comportamentul catatonic poate include:",
        options: [
            { text: "Logoree", feedback: "Incorect." },
            { text: "Flexibilitate ceroasă și stupor", feedback: "Corect. Pacientul menține poziții impuse sau e imobil." },
            { text: "Agresivitate verbală", feedback: "Incorect (poate apărea în agitație, dar flexibilitatea e specifică)." }
        ],
        correctIndex: 1
    },
    {
        question: "39. Tulburarea de personalitate schizotipală este considerată:",
        options: [
            { text: "Parte din spectrul schizofreniei", feedback: "Corect. Este o formă atenuată, premorbidă uneori." },
            { text: "O formă de manie", feedback: "Incorect." },
            { text: "O tulburare anxioasă", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "40. Alogia reprezintă:",
        options: [
            { text: "Lipsa logicii", feedback: "Incorect." },
            { text: "Sărăcia vorbirii (răspunsuri scurte, concrete)", feedback: "Corect. Simptom negativ în schizofrenie." },
            { text: "Vorbirea rapidă", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "41. Delirul de control (xenopatic) înseamnă:",
        options: [
            { text: "Pacientul crede că controlează lumea", feedback: "Incorect. Grandoare." },
            { text: "Pacientul simte că voința/acțiunile îi sunt dirijate din exterior", feedback: "Corect. 'Cineva mă teleghidează'." },
            { text: "Pacientul se verifică obsesiv", feedback: "Incorect. Obsesiv-compulsiv." }
        ],
        correctIndex: 1
    },
    {
        question: "42. Debutul schizofreniei la bărbați este de obicei:",
        options: [
            { text: "Mai precoce (15-25 ani)", feedback: "Corect. La femei debutul e mai tardiv (25-35)." },
            { text: "La vârsta a treia", feedback: "Incorect." },
            { text: "În copilăria mică", feedback: "Incorect. Foarte rar." }
        ],
        correctIndex: 0
    },
    {
        question: "43. Simptomele pozitive în schizofrenie răspund la tratament:",
        options: [
            { text: "Mai bine decât simptomele negative", feedback: "Corect. Neurolepticele reduc delirul/halucinațiile mai eficient decât avoliția." },
            { text: "Mai prost decât simptomele negative", feedback: "Incorect." },
            { text: "Nu răspund deloc", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "44. Un factor de prognostic bun în schizofrenie este:",
        options: [
            { text: "Debutul insidios (lent)", feedback: "Incorect. Debutul brusc e de prognostic bun." },
            { text: "Prezența simptomelor afective (depresie/manie)", feedback: "Corect. Forma schizoafectivă sau elementele afective indică prognostic mai bun." },
            { text: "Debutul la vârstă foarte tânără", feedback: "Incorect. Indică prognostic prost." }
        ],
        correctIndex: 1
    },
    {
        question: "45. Halucinația auditivă cea mai tipică pentru schizofrenie este:",
        options: [
            { text: "Voci care comentează acțiunile pacientului", feedback: "Corect. Sau voci care dialoghează între ele." },
            { text: "Sunete elementare (țiuituri)", feedback: "Incorect. Astea sunt mai degrabă neurologice." },
            { text: "Muzică", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    // --- CAPITOLUL 4: Tulburari afective (15 intrebari) ---
    {
        question: "46. Tulburarea Bipolară I se definește prin prezența obligatorie a:",
        options: [
            { text: "Episodului Maniacal", feedback: "Corect. Dacă a existat o singură manie, e Bipolară I." },
            { text: "Episodului Depresiv Major", feedback: "Incorect. Depresia e frecventă, dar Maniacul definește tipul I." },
            { text: "Hipomaniei", feedback: "Incorect. Hipomania definește tipul II (cu depresie)." }
        ],
        correctIndex: 0
    },
    {
        question: "47. Tulburarea Bipolară II constă în:",
        options: [
            { text: "Episoade Maniacale + Depresive", feedback: "Incorect. Asta e Tip I." },
            { text: "Episoade Hipomaniacale + Depresive Majore", feedback: "Corect. Niciodată Manie (dacă apare manie, devine Tip I)." },
            { text: "Doar episoade depresive", feedback: "Incorect (Unipolar)." }
        ],
        correctIndex: 1
    },
    {
        question: "48. Ciclotimia se caracterizează prin:",
        options: [
            { text: "Simptome hipomaniacale și depresive care nu ating pragul major", feedback: "Corect. Fluctuații timp de 2 ani." },
            { text: "Schimbări rapide de la o oră la alta", feedback: "Incorect. (Poate fi instabilitate borderline)." },
            { text: "Episoade psihotice grave", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "49. Tulburarea disforică premenstruală:",
        options: [
            { text: "Este un mit", feedback: "Incorect." },
            { text: "Apare în ultima săptămână a fazei luteale și dispare la menstruație", feedback: "Corect. E o formă de tulburare depresivă." },
            { text: "Se manifestă prin manie", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "50. Tratamentul de elecție pentru stabilizarea dispoziției în Bipolară este:",
        options: [
            { text: "Antidepresivele triciclice", feedback: "Incorect. Pot vira în manie." },
            { text: "Sărurile de Litiu sau Valproatul", feedback: "Corect. Timostabilizatoarele." },
            { text: "Benzodiazepinele", feedback: "Incorect. Sunt doar adjuvante." }
        ],
        correctIndex: 1
    },
    // --- CAPITOLUL 5: Episod expansiv (15 intrebari) ---
    {
        question: "51. Durata minimă pentru un episod Maniacal este:",
        options: [
            { text: "4 zile", feedback: "Incorect. Asta e pentru Hipomanie." },
            { text: "1 săptămână (sau orice durată dacă necesită spitalizare)", feedback: "Corect." },
            { text: "2 săptămâni", feedback: "Incorect. Asta e pentru Depresie." }
        ],
        correctIndex: 1
    },
    {
        question: "52. Diferența dintre Manie și Hipomanie este:",
        options: [
            { text: "Hipomania e mai severă", feedback: "Incorect. Hipomania e mai ușoară." },
            { text: "Mania afectează grav funcționarea sau are elemente psihotice", feedback: "Corect. Hipomania NU are elemente psihotice și nu blochează funcționarea." },
            { text: "Hipomania durează mai mult", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "53. Simptomul 'nevoie scăzută de somn' în manie înseamnă:",
        options: [
            { text: "Insomnie (vrea să doarmă dar nu poate)", feedback: "Incorect. Aceasta e în depresie/anxietate." },
            { text: "Se simte odihnit după 2-3 ore de somn", feedback: "Corect. Nu simte nevoia să doarmă." },
            { text: "Doarme toată ziua", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "54. În episodul maniacal, stima de sine este:",
        options: [
            { text: "Scăzută", feedback: "Incorect." },
            { text: "Exagerată (grandoare)", feedback: "Corect. Se crede capabil de orice." },
            { text: "Normală", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "55. YMRS (Young Mania Rating Scale) evaluează:",
        options: [
            { text: "Severitatea maniei", feedback: "Corect." },
            { text: "Riscul de suicid", feedback: "Incorect." },
            { text: "Depresia", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "56. Un scor de peste 20 la YMRS indică:",
        options: [
            { text: "Remisiune", feedback: "Incorect." },
            { text: "Probabil manie (hipomanie sau manie)", feedback: "Corect. Scorurile >20-25 indică manie." },
            { text: "Depresie severă", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "57. Logoreea în manie se caracterizează prin:",
        options: [
            { text: "Presiunea de a vorbi (vorbește mult și repede)", feedback: "Corect." },
            { text: "Vorbire rară, cu pauze lungi", feedback: "Incorect. (Bradifemie)." },
            { text: "Mutism", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "58. Activitățile 'cu potențial riscant' din manie includ:",
        options: [
            { text: "Curățenie excesivă în casă", feedback: "Incorect. (Mai degrabă obsesiv)." },
            { text: "Cheltuieli excesive, investiții necugetate, indiscreții sexuale", feedback: "Corect." },
            { text: "Privit la TV excesiv", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "59. Dispoziția în manie poate fi nu doar euforică, ci și:",
        options: [
            { text: "Iritabilă", feedback: "Corect. Mai ales când i se pun limite." },
            { text: "Apatica", feedback: "Incorect." },
            { text: "Anxioasă (exclusiv)", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    // --- CAPITOLUL 6: Episod depresiv (20 intrebari) ---
    {
        question: "60. Pentru diagnosticul de Episod Depresiv Major (DSM-5), simptomele trebuie să dureze:",
        options: [
            { text: "Minim 2 săptămâni", feedback: "Corect." },
            { text: "Minim 2 zile", feedback: "Incorect." },
            { text: "Minim 6 luni", feedback: "Incorect (doliu/tulburare adaptare)." }
        ],
        correctIndex: 0
    },
    {
        question: "61. Simptomele cheie (unul obligatoriu) în depresie sunt:",
        options: [
            { text: "Dispoziția depresivă SAU Anhedonia", feedback: "Corect. Pierderea interesului/plăcerii." },
            { text: "Insomnia sau hipersomnia", feedback: "Incorect. Sunt simptome asociate." },
            { text: "Agitația sau lentoarea", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "62. Anhedonia înseamnă:",
        options: [
            { text: "Lipsa poftei de mâncare", feedback: "Incorect (anorexie)." },
            { text: "Incapacitatea de a simți plăcere", feedback: "Corect. Nimic nu-l mai bucură." },
            { text: "Lipsa energiei", feedback: "Incorect (anergie)." }
        ],
        correctIndex: 1
    },
    {
        question: "63. Bradipsihia în depresie se manifestă prin:",
        options: [
            { text: "Gândire lentă, răspunsuri întârziate", feedback: "Corect." },
            { text: "Gândire rapidă", feedback: "Incorect (Tahipsihie)." },
            { text: "Gândire incoerentă", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "64. Delirul de ruină este specific:",
        options: [
            { text: "Maniei", feedback: "Incorect." },
            { text: "Depresiei severe (melancolice)", feedback: "Corect. Credința că a pierdut tot, că va ajunge în stradă." },
            { text: "Schizofreniei paranoide", feedback: "Incorect (acolo e persecuție)." }
        ],
        correctIndex: 1
    },
    {
        question: "65. Sindromul Cotard (delir de negație) implică:",
        options: [
            { text: "Convingerea că organele interne nu mai funcționează sau putrezesc", feedback: "Corect. Până la ideea că este mort (nemurire dureroasă)." },
            { text: "Negarea existenței lui Dumnezeu", feedback: "Incorect." },
            { text: "Refuzul de a vorbi", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "66. Riscul suicidar major în depresie apare adesea:",
        options: [
            { text: "În momentul celei mai mari inhibiții psihomotorii", feedback: "Incorect. Atunci pacientul nu are energie să acționeze." },
            { text: "La începutul ameliorării (dezinhibiție motorie)", feedback: "Corect. Când energia revine dar gândurile negre persistă." },
            { text: "După vindecarea completă", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "67. Depresia mascată se prezintă frecvent prin:",
        options: [
            { text: "Acuze somatice (dureri, tulburări digestive)", feedback: "Corect. Pacientul neagă tristețea dar acuză corpul." },
            { text: "Plâns excesiv", feedback: "Incorect (aceasta e depresie tipică)." },
            { text: "Atacuri de panică", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "68. Inventarul de Depresie Beck (BDI) este:",
        options: [
            { text: "O scală de auto-evaluare", feedback: "Corect. Pacientul completează singur." },
            { text: "O scală completată de clinician", feedback: "Incorect (Ex: Hamilton)." },
            { text: "Un test proiectiv", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "69. Scala Hamilton (HDRS) este considerată:",
        options: [
            { text: "'Standardul de aur' pentru evaluarea severității depresiei", feedback: "Corect. Folosită în studii clinice." },
            { text: "Inutilă în practică", feedback: "Incorect." },
            { text: "Specifică pentru copii", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    /* Completarea până la 100 cu întrebări mixte din capitolele 1-6 */
    {
        question: "70. Fading-ul mental (dispariția treptată a gândului) este specific:",
        options: [
            { text: "Schizofreniei", feedback: "Corect." },
            { text: "Maniei", feedback: "Incorect." },
            { text: "Anxietății", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "71. Ecolalia este:",
        options: [
            { text: "Repetarea automată a cuvintelor interlocutorului", feedback: "Corect." },
            { text: "Vorbirea cu sine însuși", feedback: "Incorect." },
            { text: "Inventarea de cuvinte noi", feedback: "Incorect (Neologism)." }
        ],
        correctIndex: 0
    },
    {
        question: "72. Catatonia este o tulburare predominant:",
        options: [
            { text: "De afectivitate", feedback: "Incorect." },
            { text: "Psihomotorie", feedback: "Corect. Implică mișcarea (imobilitate sau agitație)." },
            { text: "De memorie", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "73. Stuporul melancolic se caracterizează prin:",
        options: [
            { text: "Imobilitate totală, mutism, facies suferind", feedback: "Corect. Formă extremă de depresie." },
            { text: "Agitație extremă", feedback: "Incorect." },
            { text: "Râs nemotivat", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "74. Ambivalența afectivă înseamnă:",
        options: [
            { text: "Coexistența simultană a două emoții opuse (iubire-ură) față de aceeași persoană", feedback: "Corect. Specifică schizofreniei." },
            { text: "Lipsa oricărei emoții", feedback: "Incorect." },
            { text: "Schimbarea rapidă a emoțiilor", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "75. Halucinațiile hipnagogice apar:",
        options: [
            { text: "La adormire", feedback: "Corect. Sunt considerate fiziologice." },
            { text: "La trezire", feedback: "Incorect (Hipnapompice)." },
            { text: "În timpul zilei", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "76. Care dintre următoarele este o disomnie?",
        options: [
            { text: "Coșmarul", feedback: "Incorect (Parasomnie)." },
            { text: "Insomnia", feedback: "Corect. Tulburare a cantității/calității somnului." },
            { text: "Somnambulismul", feedback: "Incorect (Parasomnie)." }
        ],
        correctIndex: 1
    },
    {
        question: "77. Ecmnezia este:",
        options: [
            { text: "O tulburare de memorie în care trecutul este trăit ca prezent", feedback: "Corect. Pacientul se crede în altă epocă a vieții sale." },
            { text: "O pierdere a memoriei recente", feedback: "Incorect." },
            { text: "O creștere a memoriei", feedback: "Incorect (Hipermnezie)." }
        ],
        correctIndex: 0
    },
    {
        question: "78. În manie, atenția este:",
        options: [
            { text: "Hiperstabilă", feedback: "Incorect." },
            { text: "Distractibilă (instabilă)", feedback: "Corect. Sare de la un subiect la altul." },
            { text: "Absentă", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "79. Tratamentul de prevenție a recăderilor în schizofrenie:",
        options: [
            { text: "Poate fi oprit imediat ce dispar simptomele", feedback: "Incorect." },
            { text: "Trebuie menținut pe termen lung (ani sau toată viața)", feedback: "Corect." },
            { text: "Constă doar în psihoterapie", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "80. Tulburarea schizofreniformă diferă de schizofrenie prin:",
        options: [
            { text: "Durată (între 1 și 6 luni)", feedback: "Corect. Schizofrenia cere >6 luni." },
            { text: "Lipsa simptomelor psihotice", feedback: "Incorect. Are aceleași simptome." },
            { text: "Prezența maniei", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "81. Ce este 'raptusul'?",
        options: [
            { text: "O stare de meditație profundă", feedback: "Incorect." },
            { text: "O descărcare bruscă, impulsivă, violentă", feedback: "Corect. Act motor necontrolat." },
            { text: "Un tip de halucinație", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "82. Sindromul Korsakov apare frecvent în:",
        options: [
            { text: "Alcoolismul cronic", feedback: "Corect. Carență de tiamină, afectează memoria." },
            { text: "Schizofrenie", feedback: "Incorect." },
            { text: "Nevroze", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "83. Hipoestezia apare în:",
        options: [
            { text: "Manie", feedback: "Incorect. (Hiperestezie)." },
            { text: "Depresie, stări stuporoase", feedback: "Corect. Scade receptivitatea la stimuli." },
            { text: "Intoxicație cu LSD", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "84. Care simț este cel mai frecvent afectat de halucinații în schizofrenie?",
        options: [
            { text: "Vizual", feedback: "Incorect. Vizual e mai tipic pentru organicitate/alcool." },
            { text: "Auditiv", feedback: "Corect. Vocile sunt hallmark-ul." },
            { text: "Olfactiv", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "85. Dislogiile sunt:",
        options: [
            { text: "Tulburări de pronunție", feedback: "Incorect (Dislalii)." },
            { text: "Tulburări de formă și conținut ale logicii/limbajului", feedback: "Corect. Ex: neologisme, paralogisme." },
            { text: "Tulburări de scris", feedback: "Incorect (Disgrafii)." }
        ],
        correctIndex: 1
    },
    {
        question: "86. Neologismele sunt:",
        options: [
            { text: "Cuvinte noi, inventate de pacient, fără sens pentru ceilalți", feedback: "Corect." },
            { text: "Cuvinte obscene", feedback: "Incorect (Coprolalie)." },
            { text: "Repetarea ultimului cuvânt", feedback: "Incorect (Palilalie)." }
        ],
        correctIndex: 0
    },
    {
        question: "87. Gândirea magică este caracteristică tulburării:",
        options: [
            { text: "Paranoide", feedback: "Incorect." },
            { text: "Schizotipale", feedback: "Corect. Credința în superstiții, puteri paranormale." },
            { text: "Dependente", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "88. Distimia se caracterizează prin simptome depresive care durează:",
        options: [
            { text: "Cel puțin 2 ani", feedback: "Corect. Cronică, dar mai puțin severă ca Episodul Major." },
            { text: "2 săptămâni", feedback: "Incorect." },
            { text: "6 luni", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "89. Depresia de tip melancolic se agravează tipic:",
        options: [
            { text: "Dimineața", feedback: "Corect. Insomnie matinală și dispoziție proastă la trezire." },
            { text: "Seara", feedback: "Incorect. (Specific pentru depresii reactive/nevrotice uneori)." },
            { text: "Nu are variație diurnă", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "90. Ideația suicidară trebuie investigată:",
        options: [
            { text: "Doar dacă pacientul o menționează", feedback: "Incorect." },
            { text: "Sistematic, la orice pacient depresiv", feedback: "Corect. Întrebările directe nu induc suicidul, ci previn." },
            { text: "Niciodată, pentru a nu da idei", feedback: "Incorect (Mit)." }
        ],
        correctIndex: 1
    },
    {
        question: "91. Manierismele sunt:",
        options: [
            { text: "Mișcări inutile, caricaturale, bizare", feedback: "Corect." },
            { text: "Ticuri nervoase simple", feedback: "Incorect." },
            { text: "Tremurături", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "92. În schizofrenie, conștiința bolii (insight-ul):",
        options: [
            { text: "Este păstrată", feedback: "Incorect." },
            { text: "Lipsește de obicei", feedback: "Corect. Pacientul nu crede că e bolnav." },
            { text: "Este fluctuantă zilnic", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "93. Delirul de gelozie este tipic pentru:",
        options: [
            { text: "Alcoolismul cronic și paranoia", feedback: "Corect. 'Sindromul Othello'." },
            { text: "Depresie", feedback: "Incorect." },
            { text: "Fobie socială", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "94. Tulburarea afectivă sezonieră (SAD) apare de obicei:",
        options: [
            { text: "Vara", feedback: "Incorect." },
            { text: "Iarna (dispoziție depresivă legată de lumină scăzută)", feedback: "Corect." },
            { text: "Primăvara", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "95. În depresia severă poate apărea:",
        options: [
            { text: "Halucinația vizuală", feedback: "Rar." },
            { text: "Ideea delirantă de vinovăție/autoacuzare", feedback: "Corect. Congruentă cu dispoziția." },
            { text: "Ideea delirantă de grandoare", feedback: "Incorect (Incongruentă, apare în manie)." }
        ],
        correctIndex: 1
    },
    {
        question: "96. Testul ceasului (desenarea unui ceas) evaluează:",
        options: [
            { text: "Depresia", feedback: "Incorect." },
            { text: "Funcțiile cognitive/deteriorarea (demența)", feedback: "Corect. Evaluează vizuo-spațialitatea și planificarea." },
            { text: "Psihoza", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "97. Care este o cauză organică comună pentru sindromul maniacal?",
        options: [
            { text: "Hipotiroidismul", feedback: "Incorect (Dă depresie)." },
            { text: "Hipertiroidismul", feedback: "Corect. Excesul de hormoni tiroidieni agită." },
            { text: "Diabetul", feedback: "Incorect." }
        ],
        correctIndex: 1
    },
    {
        question: "98. Tulburarea de adaptare apare:",
        options: [
            { text: "Spontan, fără cauză", feedback: "Incorect." },
            { text: "Ca reacție la un stresor identificabil (ex: divorț, șomaj)", feedback: "Corect. În decurs de 3 luni de la stresor." },
            { text: "Doar în război", feedback: "Incorect (PTSD)." }
        ],
        correctIndex: 1
    },
    {
        question: "99. O caracteristică a discursului în manie este:",
        options: [
            { text: "Asociațiile prin rimă și jocuri de cuvinte", feedback: "Corect. Discurs ludic, rapid." },
            { text: "Vorbește foarte încet", feedback: "Incorect." },
            { text: "Nu vorbește deloc", feedback: "Incorect." }
        ],
        correctIndex: 0
    },
    {
        question: "100. Tratamentul electroconvulsivant (TEC) este indicat în:",
        options: [
            { text: "Nevroze ușoare", feedback: "Incorect." },
            { text: "Depresia severă cu risc suicidar iminent sau catatonie", feedback: "Corect. Când medicamentele nu funcționează sau e urgență." },
            { text: "Tulburări de personalitate", feedback: "Incorect." }
        ],
        correctIndex: 1
    }
];

let answeredCount = 0;
let score = 0;

const quizListEl = document.getElementById('quiz-list');
const answeredCountEl = document.getElementById('answered-count');
const scoreCountEl = document.getElementById('score-count');
const resetBtn = document.getElementById('reset-btn');

function initQuiz() {
    quizListEl.innerHTML = '';
    answeredCount = 0;
    score = 0;
    updateStats();

    questions.forEach((q, index) => {
        const card = createQuestionCard(q, index);
        quizListEl.appendChild(card);
    });
}

function createQuestionCard(q, index) {
    const card = document.createElement('div');
    card.classList.add('question-card');
    card.id = `q-card-${index}`;

    const header = document.createElement('div');
    header.classList.add('question-header');
    header.innerHTML = `<span class="q-badge">Întrebarea ${index + 1}</span>`;

    const title = document.createElement('h3');
    title.textContent = q.question;

    const optionsGrid = document.createElement('div');
    optionsGrid.classList.add('options-grid');

    const explanationBox = document.createElement('div');
    explanationBox.classList.add('explanation-box');
    explanationBox.id = `expl-${index}`;

    q.options.forEach((opt, optIndex) => {
        const btn = document.createElement('button');
        btn.classList.add('option-btn');
        btn.innerHTML = `${String.fromCharCode(65 + optIndex)}. ${opt.text}`;

        btn.addEventListener('click', () => {
            handleAnswer(index, optIndex, btn, q.correctIndex, explanationBox, q.options);
        });

        optionsGrid.appendChild(btn);
    });

    card.appendChild(header);
    card.appendChild(title);
    card.appendChild(optionsGrid);
    card.appendChild(explanationBox);

    return card;
}


function handleAnswer(qIndex, selectedIndex, btn, correctIndex, explanationBox, allOptions) {
    const card = document.getElementById(`q-card-${qIndex}`);
    
    // If solved (correct answer found), do not allow further interaction
    if (card.classList.contains('solved')) return;

    const isCorrect = selectedIndex === correctIndex;
    
    // Initialize attempts if needed
    if (!card.dataset.attempts) {
        card.dataset.attempts = "0";
    }

    if (isCorrect) {
        // --- Correct Logic ---
        btn.classList.add('correct');
        if (!btn.innerText.includes('✅')) btn.innerHTML += ' ✅';
        
        // Mark as solved
        card.classList.add('solved');
        
        // Disable all buttons
        const buttons = card.querySelectorAll('.option-btn');
        buttons.forEach(b => b.disabled = true);

        // Update Score only if first attempt
        if (parseInt(card.dataset.attempts) === 0) {
            score++;
        }
        
        answeredCount++;
        updateStats();

        // Show Correct Feedback
        const feedbackText = allOptions[selectedIndex].feedback;
        explanationBox.innerHTML = `<strong style="color:var(--success-color)">Corect!</strong> ${feedbackText}`;
        explanationBox.classList.remove('incorrect-feedback');
        explanationBox.classList.add('visible');
        explanationBox.style.borderLeft = "4px solid var(--success-color)";
        // explanationBox.style.backgroundColor = "var(--success-bg)"; // CSS handles transparency better usually, removed inline style to rely on CSS classes if possible, but keeping inline valid for overriding.

    } else {
        // --- Incorrect Logic ---
        btn.classList.add('incorrect');
        if (!btn.innerText.includes('❌')) btn.innerHTML += ' ❌';
        btn.disabled = true; // Disable just this one
        
        // Increment attempts
        card.dataset.attempts = parseInt(card.dataset.attempts) + 1;

        // Show Incorrect Feedback
        const feedbackText = allOptions[selectedIndex].feedback;
        explanationBox.innerHTML = `<strong style="color:var(--error-color)">Incorect.</strong> ${feedbackText} <div style="margin-top:0.5rem; font-size:0.85em; opacity:0.8">Mai încearcă!</div>`;
        explanationBox.classList.add('visible');
        explanationBox.classList.add('incorrect-feedback');
        explanationBox.style.borderLeft = "4px solid var(--error-color)";
    }
}

function updateStats() {
    answeredCountEl.textContent = answeredCount;
    scoreCountEl.textContent = score;
}

resetBtn.addEventListener('click', () => {
    if (confirm('Sigur dorești să resetezi tot testul? Progresul va fi pierdut.')) {
        window.scrollTo(0, 0);
        initQuiz();
    }
});

// Initialize on load
initQuiz();
