document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let currentUploadedFile = null;
    const BASE_URL = 'https://legal-document-rag.onrender.com';
    // --- DOM Elements ---
    // Navigation
    const navDashboard = document.getElementById('nav-dashboard');
    const navChat = document.getElementById('nav-chat');
    const dashboardView = document.getElementById('dashboard-view');
    const chatView = document.getElementById('chat-view');

    // Upload
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    
    // Actions
    const btnSummarize = document.getElementById('btn-summarize');
    const btnRedflag = document.getElementById('btn-redflag');
    const resultsContainer = document.getElementById('results-container');

    // Chat
    const chatInput = document.getElementById('chat-input');
    const btnSendChat = document.getElementById('btn-send-chat');
    const chatHistory = document.getElementById('chat-history');

    // --- Navigation Logic ---
    navDashboard.addEventListener('click', (e) => {
        e.preventDefault();
        navDashboard.classList.add('active');
        navChat.classList.remove('active');
        dashboardView.classList.remove('hidden');
        chatView.classList.add('hidden');
    });

    navChat.addEventListener('click', (e) => {
        e.preventDefault();
        navChat.classList.add('active');
        navDashboard.classList.remove('active');
        chatView.classList.remove('hidden');
        dashboardView.classList.add('hidden');
    });

    // --- Upload Logic ---
    browseBtn.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith('.pdf')) {
            alert("Please upload a PDF file.");
            return;
        }

        dropZone.innerHTML = `<div class="loader"></div><p style="margin-top: 15px">Uploading and processing...</p>`;
        
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            const responseText = await response.text();
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                throw new Error(`Server returned non-JSON response. Status: ${response.status}. Raw output: ${responseText.slice(0, 150)}`);
            }
            
            if (response.ok) {
                currentUploadedFile = data.filename || file.name;
                currentUploadedFile = currentUploadedFile.split('/').pop() || currentUploadedFile; 
                
                // Update UI state
                dropZone.innerHTML = `
                    <i class="fa-solid fa-file-circle-check drop-icon" style="color: var(--accent-green)"></i>
                    <p style="margin-top: 15px">Successfully uploaded:</p>
                    <h4 style="color: var(--text-primary); margin-top: 5px;">${currentUploadedFile}</h4>
                `;
                
                // Enable action buttons
                btnSummarize.disabled = false;
                btnRedflag.disabled = false;

                // Set focus to actions
                resultsContainer.innerHTML = `
                    <div class="empty-state">
                        <i class="fa-solid fa-check-circle" style="color: var(--accent-green)"></i>
                        <p>Document ready. Select an action to begin analysis.</p>
                    </div>
                `;
            } else {
                throw new Error(data.detail || "Upload failed");
            }
        } catch (error) {
            console.error(error);
            dropZone.innerHTML = `
                <i class="fa-solid fa-circle-xmark drop-icon" style="color: var(--accent-red)"></i>
                <p style="margin-top: 15px">Upload Failed. Error: ${error.message}</p>
                <button class="btn btn-primary" onclick="document.getElementById('file-input').click()" style="margin-top:10px;">Browse</button>
            `;
        }
    }

    // --- Actions Logic ---
    function showLoadingResults(text) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="loader"></div>
                <p style="margin-top: 15px">${text}...</p>
            </div>
        `;
    }

    btnSummarize.addEventListener('click', async () => {
        if (!currentUploadedFile) return;
        
        const originalHtml = btnSummarize.innerHTML;
        btnSummarize.innerHTML = '<div class="btn-loader"></div>';
        btnSummarize.disabled = true;
        showLoadingResults("Generating professional summary");

        try {
            const response = await fetch(`${BASE_URL}/summary`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: currentUploadedFile })
            });

            const data = await response.json();
            if (response.ok) {
                // Determine property name based on backend return (e.g., result_summary or summary)
                const summaryText = data.result_summary || data.summary || "No summary returned.";
                resultsContainer.innerHTML = `
                    <h4 style="color: var(--accent-blue); margin-bottom: 15px;"><i class="fa-solid fa-file-lines"></i> Document Summary</h4>
                    <div class="result-text">${summaryText}</div>
                `;
            } else {
                throw new Error(data.detail || "Summarization failed");
            }
        } catch (error) {
            resultsContainer.innerHTML = `<div class="result-text" style="color: var(--accent-red)"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}</div>`;
        } finally {
            btnSummarize.innerHTML = originalHtml;
            btnSummarize.disabled = false;
        }
    });

    btnRedflag.addEventListener('click', async () => {
        if (!currentUploadedFile) return;
        
        const originalHtml = btnRedflag.innerHTML;
        btnRedflag.innerHTML = '<div class="btn-loader"></div>';
        btnRedflag.disabled = true;
        showLoadingResults("Analyzing potential risks and red flags");

        try {
            const response = await fetch(`${BASE_URL}/redflag`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: currentUploadedFile })
            });

            const data = await response.json();
            if (response.ok) {
                const risks = data["red flags"] || data.red_flags || "No risks detected.";
                resultsContainer.innerHTML = `
                    <h4 style="color: var(--accent-red); margin-bottom: 15px;"><i class="fa-solid fa-triangle-exclamation"></i> Risk Analysis</h4>
                    <div class="result-text">${risks}</div>
                `;
            } else {
                throw new Error(data.detail || "Analysis failed");
            }
        } catch (error) {
            resultsContainer.innerHTML = `<div class="result-text" style="color: var(--accent-red)"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}</div>`;
        } finally {
            btnRedflag.innerHTML = originalHtml;
            btnRedflag.disabled = false;
        }
    });

    // --- Chat Logic ---
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;
        
        const avatarStr = sender === 'user' 
            ? '<i class="fa-solid fa-user"></i>' 
            : '<i class="fa-solid fa-scale-balanced"></i>';
            
        messageDiv.innerHTML = `
            <div class="avatar">${avatarStr}</div>
            <div class="message-content">${text}</div>
        `;
        
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function sendChatMessage() {
        const question = chatInput.value.trim();
        if (!question) return;

        appendMessage('user', question);
        chatInput.value = '';
        
        // Show typing indicator
        const typingId = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = `chat-message bot-message`;
        typingDiv.id = typingId;
        typingDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-scale-balanced"></i></div>
            <div class="message-content" style="padding: 10px 15px;"><div class="loader" style="width: 16px; height: 16px; border-width: 2px;"></div></div>
        `;
        chatHistory.appendChild(typingDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const response = await fetch(`${BASE_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question }) // Match "question" exactly with Pydantic model
            });

            const data = await response.json();
            
            // Remove typing indicator
            document.getElementById(typingId).remove();
            
            if (response.ok) {
                appendMessage('bot', data.answer);
            } else {
                throw new Error(data.detail || "Failed to get answer");
            }
        } catch (error) {
            document.getElementById(typingId).remove();
            appendMessage('bot', `Error: ${error.message}`);
        }
    }

    btnSendChat.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
});
