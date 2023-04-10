
const searchInput = document.getElementById("search");
const micButton = document.getElementById("micButton");

if (window.SpeechRecognition || window.webkitSpeechRecognition) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = "ko-KR";

    function showOverlay() {
        document.getElementById("overlay").style.display = "block";
    }
    
    function hideOverlay() {
        document.getElementById("overlay").style.display = "none";
    }



    micButton.addEventListener("click", async () => {
        try {
            await navigator.mediaDevices.getUserMedia({ audio: true });
            showOverlay(); // 마이크 사용 시작 시 오버레이 표시
            recognition.start();
        } catch (error) {
            console.error("Error accessing microphone: ", error);
        }
    });
    
    recognition.addEventListener("result", (event) => {
        const transcript = event.results[0][0].transcript;
        searchInput.value = transcript;

        hideOverlay(); // 음성 인식 완료 시 오버레이 숨기기

        

        // 폼을 자동으로 제출합니다.
        const searchForm = document.querySelector(".search-box");
        searchForm.submit();
    });
    
    recognition.addEventListener("error", (event) => {
        console.error("Error occurred in recognition: " + event.error);
        hideOverlay(); // 오류 발생 시 오버레이 숨기기
    });

    const cancelButton = document.getElementById("cancelButton");

    cancelButton.addEventListener("click", () => {
        recognition.stop(); // 마이크 사용 취소 버튼을 누르면 음성 인식을 멈춥니다.
        hideOverlay(); // 마이크 사용 취소 버튼을 누르면 오버레이를 숨깁니다.
    });

    



    // micButton.addEventListener("click", async () => {
    //     try {
    //         await navigator.mediaDevices.getUserMedia({ audio: true });
    //         recognition.start();
    //     } catch (error) {
    //         console.error("Error accessing microphone: ", error);
    //     }
    // });

    // recognition.addEventListener("result", (event) => {
    //     const transcript = event.results[0][0].transcript;
    //     searchInput.value = transcript;

    //     // 폼을 자동으로 제출합니다.
    //     const searchForm = document.querySelector(".search-box");
    //     searchForm.submit();
    // });

    // recognition.addEventListener("error", (event) => {
    //     console.error("Error occurred in recognition: " + event.error);
    // });
} else {
    micButton.disabled = true;
    console.warn("SpeechRecognition is not supported in this browser.");
}
