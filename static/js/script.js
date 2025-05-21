document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const tabButtons = document.querySelectorAll('.tab-btn');
    const counterargumentsDesc = document.querySelector('.counterarguments-desc');
    const fallaciesDesc = document.querySelector('.fallacies-desc');
    const analyzeBtn = document.getElementById('analyze-btn');
    const debateTopic = document.getElementById('debate-topic');
    const perspective = document.getElementById('perspective');
    const resultsContainer = document.getElementById('results-container');
    const resultsText = document.getElementById('results-text');
    const loadingSpinner = document.getElementById('loading-spinner');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');
    
    // Current active mode
    let currentMode = 'counterarguments';
    
    // Tab button click handler
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update current mode
            currentMode = this.dataset.mode;
            
            // Toggle description visibility
            if (currentMode === 'counterarguments') {
                counterargumentsDesc.classList.add('active');
                fallaciesDesc.classList.remove('active');
            } else {
                counterargumentsDesc.classList.remove('active');
                fallaciesDesc.classList.add('active');
            }
        });
    });
    
    // Form submission handler
    analyzeBtn.addEventListener('click', function() {
        const topic = debateTopic.value.trim();
        
        if (!topic) {
            showNotification('Please enter a debate topic', 'error');
            return;
        }
        
        // Show loading state
        resultsContainer.style.display = 'block';
        loadingSpinner.style.display = 'flex';
        resultsText.innerHTML = '';
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
        
        // Prepare data for API call
        const debateData = {
            topic: topic,
            perspective: perspective.value.trim(),
            mode: currentMode
        };
        
        // Make API call to backend
        fetchAnalysis(debateData);
    });
    
    // Copy results to clipboard
    copyBtn.addEventListener('click', function() {
        const textToCopy = resultsText.innerText;
        
        if (textToCopy) {
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    showNotification('Results copied to clipboard!', 'success');
                })
                .catch(err => {
                    showNotification('Failed to copy text', 'error');
                    console.error('Could not copy text: ', err);
                });
        }
    });
    
    // Download results as PDF
    downloadBtn.addEventListener('click', function() {
        const resultsContent = resultsText.innerText;
        
        if (!resultsContent) return;
        
        // Create a Blob with the content
        const blob = new Blob([resultsContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        // Create temporary link and trigger download
        const a = document.createElement('a');
        a.href = url;
        a.download = 'debate-analysis.txt';
        document.body.appendChild(a);
        a.click();
        
        // Clean up
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
        
        showNotification('Results downloaded!', 'success');
    });
    
    // Function to fetch analysis from backend API
    async function fetchAnalysis(debateData) {
        try {
            console.log('Sending debate data:', debateData);
            
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(debateData)
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API error response:', errorText);
                throw new Error(`HTTP error! Status: ${response.status}, Response: ${errorText}`);
            }
            
            const data = await response.json();
            console.log('API response:', data);
            
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            // Check if result exists
            if (!data || !data.result) {
                throw new Error("Invalid response format - missing result data");
            }
            
            // Display results
            displayResults(data.result);
            
        } catch (error) {
            console.error('Error fetching analysis:', error);
            loadingSpinner.style.display = 'none';
            resultsText.innerHTML = `<div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error analyzing debate. Please try again later.</p>
                <p class="error-details">${error.message}</p>
            </div>`;
            
            // Show error notification
            showNotification('Error: ' + error.message, 'error');
        }
    }
    
    // Function to display results with formatting
    function displayResults(results) {
        // Convert line breaks to HTML breaks and add some simple formatting
        const formattedResults = results
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
            .replace(/\*(.*?)\*/g, '<em>$1</em>');  // Italic text
        
        resultsText.innerHTML = `<p>${formattedResults}</p>`;
    }
    
    // Toast notification system
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existing = document.querySelector('.notification');
        if (existing) {
            existing.remove();
        }
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        // Add icon based on type
        let icon = 'info-circle';
        if (type === 'success') icon = 'check-circle';
        if (type === 'error') icon = 'exclamation-circle';
        
        notification.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
        `;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.add('active');
        }, 10);
        
        // Remove after delay
        setTimeout(() => {
            notification.classList.remove('active');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Add notification styling
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background-color: #f8f9fa;
            border-left: 4px solid #4a6fa5;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            z-index: 1000;
            transform: translateX(120%);
            transition: transform 0.3s ease;
            max-width: 90%;
        }
        
        .notification.active {
            transform: translateX(0);
        }
        
        .notification i {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        
        .notification.success {
            border-left-color: #28a745;
        }
        
        .notification.success i {
            color: #28a745;
        }
        
        .notification.error {
            border-left-color: #dc3545;
        }
        
        .notification.error i {
            color: #dc3545;
        }
        
        .error-message {
            color: #dc3545;
            text-align: center;
            padding: 20px;
        }
        
        .error-message i {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        
        .error-details {
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: 10px;
        }
    `;
    document.head.appendChild(style);
});