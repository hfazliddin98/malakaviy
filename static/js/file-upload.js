// Fayl yuklash funksiyalari

class FileUploader {
    constructor() {
        this.maxSize = 4 * 1024 * 1024; // 4MB
        this.allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        this.allowedExtensions = ['pdf', 'doc', 'docx', 'wps'];
        this.init();
    }

    init() {
        this.setupFileInputs();
        this.setupDragAndDrop();
    }

    setupFileInputs() {
        const fileInputs = document.querySelectorAll('input[type="file"]:not([name="pasport"])');
        
        fileInputs.forEach(input => {
            const container = this.createFileUploadContainer(input);
            input.parentNode.replaceChild(container, input);
            
            const newInput = container.querySelector('input[type="file"]');
            newInput.addEventListener('change', (e) => this.handleFileSelect(e));
        });

        // Pasport fayli uchun maxsus ishlov berish
        const pasportInput = document.querySelector('input[name="pasport"]');
        if (pasportInput) {
            pasportInput.addEventListener('change', (e) => this.handlePassportSelect(e));
        }
    }

    createFileUploadContainer(originalInput) {
        const container = document.createElement('div');
        container.className = 'file-upload-container';
        
        const wrapper = document.createElement('div');
        wrapper.className = 'file-upload-wrapper';
        
        const button = document.createElement('div');
        button.className = 'file-upload-button';
        button.innerHTML = `
            <i class="fas fa-cloud-upload-alt file-upload-icon"></i>
            <span class="file-upload-text">Fayl tanlang yoki shu yerga tashlang</span>
        `;
        
        const input = originalInput.cloneNode(true);
        input.className = 'file-upload-input';
        
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        
        const progressBar = document.createElement('div');
        progressBar.className = 'upload-progress';
        progressBar.innerHTML = '<div class="upload-progress-bar"></div>';
        
        wrapper.appendChild(input);
        wrapper.appendChild(button);
        container.appendChild(wrapper);
        container.appendChild(fileInfo);
        container.appendChild(progressBar);
        
        return container;
    }

    handleFileSelect(event) {
        const input = event.target;
        const file = input.files[0];
        const container = input.closest('.file-upload-container');
        const button = container.querySelector('.file-upload-button');
        const fileInfo = container.querySelector('.file-info');
        const progressBar = container.querySelector('.upload-progress');
        
        if (!file) {
            this.resetFileInput(container);
            return;
        }

        // Fayl validatsiyasi
        const validation = this.validateFile(file);
        if (!validation.valid) {
            this.showError(container, validation.error);
            input.value = '';
            return;
        }

        // Muvaffaqiyatli yuklangan fayl ko'rinishi
        button.classList.add('has-file');
        button.innerHTML = `
            <i class="fas fa-check file-upload-icon"></i>
            <span class="file-upload-text">${file.name}</span>
            <a href="#" class="remove-file" onclick="fileUploader.removeFile(this, event)">
                <i class="fas fa-times"></i>
            </a>
        `;

        // Fayl ma'lumotlari
        fileInfo.innerHTML = `
            <div class="d-flex justify-content-between">
                <span>Fayl: ${file.name}</span>
                <span class="file-size">${this.formatFileSize(file.size)}</span>
            </div>
        `;
        fileInfo.classList.add('show');

        // Progress bar animatsiyasi
        this.animateProgress(progressBar);
    }

    handlePassportSelect(event) {
        const input = event.target;
        const file = input.files[0];
        
        if (!file) return;

        // Pasport fayli uchun maxsus validatsiya
        if (file.size > this.maxSize) {
            alert('Pasport fayli 4MB dan katta bo\'lmasligi kerak!');
            input.value = '';
            return;
        }

        const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedImageTypes.includes(file.type)) {
            alert('Pasport fayli JPG, JPEG yoki PNG formatida bo\'lishi kerak!');
            input.value = '';
            return;
        }
    }

    validateFile(file) {
        // Fayl hajmi tekshirish
        if (file.size > this.maxSize) {
            return {
                valid: false,
                error: `Fayl hajmi ${this.formatFileSize(this.maxSize)} dan oshmasligi kerak!`
            };
        }

        // Fayl formati tekshirish
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (!this.allowedExtensions.includes(fileExtension)) {
            return {
                valid: false,
                error: `Faqat ${this.allowedExtensions.join(', ').toUpperCase()} formatlar qabul qilinadi!`
            };
        }

        return { valid: true };
    }

    showError(container, message) {
        const button = container.querySelector('.file-upload-button');
        const fileInfo = container.querySelector('.file-info');
        
        button.classList.add('error');
        button.innerHTML = `
            <i class="fas fa-exclamation-triangle file-upload-icon"></i>
            <span class="file-upload-text">Xato!</span>
        `;

        fileInfo.innerHTML = `<div class="file-error">${message}</div>`;
        fileInfo.classList.add('show');

        // Xatoni 5 soniyadan keyin o'chirish
        setTimeout(() => {
            this.resetFileInput(container);
        }, 5000);
    }

    resetFileInput(container) {
        const button = container.querySelector('.file-upload-button');
        const fileInfo = container.querySelector('.file-info');
        const progressBar = container.querySelector('.upload-progress');
        
        button.className = 'file-upload-button';
        button.innerHTML = `
            <i class="fas fa-cloud-upload-alt file-upload-icon"></i>
            <span class="file-upload-text">Fayl tanlang yoki shu yerga tashlang</span>
        `;
        
        fileInfo.classList.remove('show');
        progressBar.classList.remove('show');
    }

    removeFile(element, event) {
        event.preventDefault();
        const container = element.closest('.file-upload-container');
        const input = container.querySelector('input[type="file"]');
        
        input.value = '';
        this.resetFileInput(container);
    }

    animateProgress(progressBar) {
        progressBar.classList.add('show');
        const bar = progressBar.querySelector('.upload-progress-bar');
        
        let width = 0;
        const interval = setInterval(() => {
            width += Math.random() * 15;
            if (width >= 100) {
                width = 100;
                clearInterval(interval);
                setTimeout(() => {
                    progressBar.classList.remove('show');
                }, 1000);
            }
            bar.style.width = width + '%';
        }, 50);
    }

    setupDragAndDrop() {
        const containers = document.querySelectorAll('.file-upload-container');
        
        containers.forEach(container => {
            const wrapper = container.querySelector('.file-upload-wrapper');
            const input = container.querySelector('input[type="file"]');
            
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                wrapper.addEventListener(eventName, this.preventDefaults, false);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                wrapper.addEventListener(eventName, () => this.highlight(wrapper), false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                wrapper.addEventListener(eventName, () => this.unhighlight(wrapper), false);
            });

            wrapper.addEventListener('drop', (e) => this.handleDrop(e, input), false);
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    highlight(element) {
        element.classList.add('drag-over');
    }

    unhighlight(element) {
        element.classList.remove('drag-over');
    }

    handleDrop(e, input) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            input.files = files;
            const event = new Event('change', { bubbles: true });
            input.dispatchEvent(event);
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Form yuborish vaqtida loading ko'rsatish
function handleFormSubmit(form) {
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
    if (submitBtn) {
        submitBtn.classList.add('btn-loading');
        submitBtn.disabled = true;
        
        // 30 soniyadan keyin loading'ni o'chirish (xatolik holatida)
        setTimeout(() => {
            submitBtn.classList.remove('btn-loading');
            submitBtn.disabled = false;
        }, 30000);
    }
}

// Sahifa yuklanganda ishga tushirish
document.addEventListener('DOMContentLoaded', function() {
    window.fileUploader = new FileUploader();
    
    // Form submit events
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', () => handleFormSubmit(form));
    });
});

// Global funksiya (inline onclick uchun)
function removeFile(element, event) {
    if (window.fileUploader) {
        window.fileUploader.removeFile(element, event);
    }
}