document.addEventListener('DOMContentLoaded', () => {
    const commentForm = document.getElementById('commentForm');
    const commentsContainer = document.getElementById('commentsContainer');
    
    commentForm.addEventListener('submit', (event) => {
        event.preventDefault(); // 防止表單提交頁面重新加載
        
        const commentInput = document.getElementById('commentInput');
        const commentText = commentInput.value;
        
        if (commentText.trim() === "") return; // 防止空評論
        
        // 創建評論元素
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerText = commentText;

        // 添加時間戳
        const date = new Date();
        const time = date.toLocaleString(); // 可根據需要格式化時間
        const timeElement = document.createElement('span');
        timeElement.className = 'comment-time';
        timeElement.innerText = time;

        commentElement.appendChild(timeElement);
        commentsContainer.appendChild(commentElement);

        // 清空輸入框
        commentInput.value = '';
    });
});
