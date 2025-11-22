document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.getElementById('draft-title');
    const contentEditor = document.getElementById('draft-content');
    const saveStatus = document.getElementById('save-status');
    const draftId = contentEditor.dataset.draftId;

    let saveTimeout;
    let isSaving = false;

    // 自动保存功能
    function autoSave() {
        if (isSaving) return;

        isSaving = true;
        saveStatus.textContent = '保存中...';
        saveStatus.style.background = '#ffc107';

        const data = {
            title: titleInput.value,
            content: contentEditor.innerHTML
        };

        fetch(`/author/draft/${draftId}/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                saveStatus.textContent = '已保存';
                saveStatus.style.background = '#28a745';
            } else {
                saveStatus.textContent = '保存失败';
                saveStatus.style.background = '#dc3545';
            }
            isSaving = false;
        })
        .catch(error => {
            console.error('保存失败:', error);
            saveStatus.textContent = '保存失败';
            saveStatus.style.background = '#dc3545';
            isSaving = false;
        });
    }

    // 防抖保存
    function debounceSave() {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(autoSave, 1000);
    }

    // 监听输入事件
    titleInput.addEventListener('input', debounceSave);
    contentEditor.addEventListener('input', debounceSave);

    // 工具栏功能
    document.querySelectorAll('.toolbar-btn[data-command]').forEach(btn => {
        btn.addEventListener('click', function() {
            const command = this.dataset.command;
            document.execCommand(command, false, null);
            contentEditor.focus();
        });
    });

    // AI助手功能
    const aiModal = document.getElementById('ai-modal');
    const aiAssistBtn = document.getElementById('ai-assist-btn');
    const aiSuggestBtn = document.getElementById('ai-suggest-btn');
    const closeModal = document.querySelector('.close-modal');
    const aiCancel = document.getElementById('ai-cancel');
    const aiGenerate = document.getElementById('ai-generate');
    const aiInsert = document.getElementById('ai-insert');
    const aiCopy = document.getElementById('ai-copy');
    const aiResult = document.getElementById('ai-result');

    function openAiModal() {
        aiModal.style.display = 'block';
    }

    function closeAiModal() {
        aiModal.style.display = 'none';
        aiResult.style.display = 'none';
        document.getElementById('ai-prompt').value = '';
        document.getElementById('ai-context').value = '';
    }

    aiAssistBtn.addEventListener('click', openAiModal);
    aiSuggestBtn.addEventListener('click', openAiModal);
    closeModal.addEventListener('click', closeAiModal);
    aiCancel.addEventListener('click', closeAiModal);

    // 点击模态框外部关闭
    window.addEventListener('click', function(event) {
        if (event.target === aiModal) {
            closeAiModal();
        }
    });

    aiGenerate.addEventListener('click', function() {
        const prompt = document.getElementById('ai-prompt').value;
        const context = document.getElementById('ai-context').value;

        if (!prompt.trim()) {
            alert('请输入你的请求');
            return;
        }

        aiGenerate.disabled = true;
        aiGenerate.textContent = '生成中...';

        fetch('/author/ai/assist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                context: context
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                document.querySelector('.ai-content').textContent = result.result;
                aiResult.style.display = 'block';
            } else {
                alert('AI请求失败: ' + result.error);
            }
        })
        .catch(error => {
            alert('请求失败: ' + error);
        })
        .finally(() => {
            aiGenerate.disabled = false;
            aiGenerate.textContent = '生成';
        });
    });

    aiInsert.addEventListener('click', function() {
        const aiContent = document.querySelector('.ai-content').textContent;
        document.execCommand('insertText', false, aiContent);
        closeAiModal();
    });

    aiCopy.addEventListener('click', function() {
        const aiContent = document.querySelector('.ai-content').textContent;
        navigator.clipboard.writeText(aiContent).then(() => {
            alert('已复制到剪贴板');
        });
    });

    // 键盘快捷键
    document.addEventListener('keydown', function(e) {
        // Ctrl+S 保存
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            autoSave();
        }
    });

    // 内容编辑器粘贴处理
    contentEditor.addEventListener('paste', function(e) {
        e.preventDefault();
        const text = e.clipboardData.getData('text/plain');
        document.execCommand('insertText', false, text);
    });
});
