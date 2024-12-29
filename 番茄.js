document.addEventListener("DOMContentLoaded", () => {
    const growthStages = [
        { time: 0, scale: 1, image: "番茄/1.png" },
        { time: 5, scale: 1.5, image: "番茄/2.png" },
        { time: 10, scale: 2, image: "番茄/3.png" },
        { time: 15, scale: 2.5, image: "番茄/4.png" },
        { time: 20, scale: 3, image: "番茄/5.png" },
    ];

    const tomato = document.getElementById("tomato");
    const tomatoContainer = document.getElementById("tomato-container");

    if (!tomato) {
        console.error('Element with id="tomato" not found.');
        return;
    }

    if (!tomatoContainer) {
        console.error('Element with id="tomato-container" not found.');
        return;
    }

    console.log("Tomato element:", tomato);

    let startTime = Date.now();
    let lastImage = "番茄/1.png"; // 用來追踪上一次顯示的圖片

    const interval = setInterval(updateTomatoGrowth, 1000); // 每秒檢查一次

    function updateTomatoGrowth() {
        const elapsedTime = Math.floor((Date.now() - startTime) / 1000); // 經過的秒數
        const currentStage = growthStages.find((stage, index) =>
            elapsedTime >= stage.time &&
            (index === growthStages.length - 1 || elapsedTime < growthStages[index + 1].time)
        );

        if (currentStage) {
            const containerWidth = tomatoContainer.offsetWidth;
            const containerHeight = tomatoContainer.offsetHeight;

            // 計算最大縮放比例，避免圖片超出容器範圍
            const maxScale = Math.min(containerWidth / 100, containerHeight / 150);

            let scale = currentStage.scale;
            scale = Math.min(scale, maxScale); // 限制最大縮放比例

            tomato.style.transform = `scale(${scale})`;

            // 只在圖片發生變化時執行過渡
            if (currentStage.image !== lastImage) {
                tomato.style.opacity = 0; // 淡出當前圖片

                setTimeout(() => {
                    tomato.src = currentStage.image;
                    tomato.style.opacity = 1; // 淡入新圖片
                    lastImage = currentStage.image; // 更新上一次顯示的圖片
                }, 500); // 等待淡出完成
            }
        }

        if (elapsedTime >= growthStages[growthStages.length - 1].time + 5) {
            clearInterval(interval); // 停止更新
            console.log("Animation complete.");
        }
    }
});
