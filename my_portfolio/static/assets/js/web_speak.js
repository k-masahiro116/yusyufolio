const speakBtn = document.querySelector('#speak-btn')

        speakBtn.addEventListener('click', function() {
            // 発言を作成
            text = "こんにちは、私はまさひろと言います。"
            const uttr = new SpeechSynthesisUtterance(text)
            // 発言を再生 (発言キューに発言を追加)
            speechSynthesis.speak(uttr)
        })