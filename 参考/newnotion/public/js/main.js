document.addEventListener("DOMContentLoaded", () => {
  // --- STATE MANAGEMENT ---
  const state = {
    notes: [],
    activeNoteId: null,
  };

  // --- DOM ELEMENT REFERENCES ---
  const dom = {
    notesList: document.getElementById("notes-list"),
    newNoteBtn: document.getElementById("new-note-btn"),
    editorView: document.getElementById("editor-view"),
    welcomeView: document.getElementById("welcome-view"),
    noteTitle: document.getElementById("note-title"),
    noteContent: document.getElementById("note-content"),
    settingsBtn: document.getElementById("settings-btn"),
    settingsModal: document.getElementById("settings-modal"),
    closeModalBtn: document.getElementById("close-modal-btn"),
    saveSettingsBtn: document.getElementById("save-settings-btn"),
    apiUrlInput: document.getElementById("api-url"),
    apiKeyInput: document.getElementById("api-key"),
    modelNameInput: document.getElementById("model-name"),
    aiAssistBtn: document.getElementById("ai-assist-btn"),
  };

  // --- API HELPER FUNCTIONS ---
  const api = {
    async getNotes() {
      const response = await fetch("/api/notes");
      if (!response.ok) throw new Error("Failed to fetch notes");
      return response.json();
    },
    async createNote() {
      const response = await fetch("/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: "New Note", content: "" }),
      });
      if (!response.ok) throw new Error("Failed to create note");
      return response.json();
    },
    async updateNote(id, { title, content }) {
      const response = await fetch(`/api/notes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content }),
      });
      if (!response.ok) throw new Error("Failed to update note");
      return response.json();
    },
    async deleteNote(id) {
      const response = await fetch(`/api/notes/${id}`, {
        method: "DELETE",
      });
      if (!response.ok && response.status !== 204) {
        throw new Error("Failed to delete note");
      }
    },
  };

  // --- RENDER FUNCTIONS ---
  const renderNotesList = () => {
    dom.notesList.innerHTML = "";
    if (state.notes.length === 0) {
      dom.notesList.innerHTML =
        '<p class="no-notes">No notes yet. Create one!</p>';
      return;
    }
    state.notes.forEach((note) => {
      const item = document.createElement("div");
      item.className = "note-item";
      item.dataset.id = note.id;
      if (note.id === state.activeNoteId) {
        item.classList.add("active");
      }
      item.innerHTML = `
                <span class="note-item-title">${note.title || "Untitled"}</span>
                <span class="note-item-date">${formatDate(note.updatedAt)}</span>
            `;
      dom.notesList.appendChild(item);
    });
  };

  const renderEditor = () => {
    const activeNote = state.notes.find(
      (note) => note.id === state.activeNoteId,
    );
    if (activeNote) {
      dom.welcomeView.style.display = "none";
      dom.editorView.style.display = "flex";
      dom.noteTitle.value = activeNote.title;
      dom.noteContent.value = activeNote.content;
    } else {
      dom.editorView.style.display = "none";
      dom.welcomeView.style.display = "flex";
    }
  };

  // --- EVENT HANDLERS ---
  const handleNewNote = async () => {
    const newNote = await api.createNote();
    state.notes.unshift(newNote);
    state.activeNoteId = newNote.id;
    renderNotesList();
    renderEditor();
    dom.noteTitle.focus();
  };

  const handleNoteSelection = (e) => {
    const noteItem = e.target.closest(".note-item");
    if (noteItem) {
      const noteId = parseInt(noteItem.dataset.id, 10);
      if (state.activeNoteId !== noteId) {
        state.activeNoteId = noteId;
        renderNotesList();
        renderEditor();
      }
    }
  };

  const debouncedUpdate = debounce(async () => {
    if (!state.activeNoteId) return;

    const title = dom.noteTitle.value;
    const content = dom.noteContent.value;

    const updatedNote = await api.updateNote(state.activeNoteId, {
      title,
      content,
    });

    const noteIndex = state.notes.findIndex((n) => n.id === state.activeNoteId);
    if (noteIndex > -1) {
      state.notes[noteIndex] = updatedNote;
      // Re-sort and render to reflect the new updatedAt timestamp
      state.notes.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
      renderNotesList();
    }
  }, 500);

  const handleSettingsToggle = (show) => {
    if (show) {
      loadSettings();
      dom.settingsModal.style.display = "flex";
    } else {
      dom.settingsModal.style.display = "none";
    }
  };

  const handleSaveSettings = () => {
    const settings = {
      apiUrl: dom.apiUrlInput.value,
      apiKey: dom.apiKeyInput.value,
      modelName: dom.modelNameInput.value,
    };
    localStorage.setItem("aiSettings", JSON.stringify(settings));
    handleSettingsToggle(false);
  };

  const handleAiAssist = async () => {
    const settings = JSON.parse(localStorage.getItem("aiSettings"));
    if (!settings || !settings.apiUrl || !settings.apiKey) {
      alert("Please configure your AI settings first.");
      handleSettingsToggle(true);
      return;
    }

    const selection = dom.noteContent.value.substring(
      dom.noteContent.selectionStart,
      dom.noteContent.selectionEnd,
    );
    const prompt = selection || dom.noteContent.value;

    if (!prompt) {
      alert("Please write something or select text to use the AI assistant.");
      return;
    }

    dom.aiAssistBtn.textContent = "...";
    dom.aiAssistBtn.disabled = true;

    try {
      const response = await fetch("/api/ai-assist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt, settings }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.details || error.error);
      }

      const data = await response.json();
      const resultText = data.choices[0].message.content;

      // Append result to the content
      dom.noteContent.value += `\n\n${resultText}`;
      debouncedUpdate(); // Save the note
    } catch (error) {
      console.error("AI Assist Error:", error);
      alert(`An error occurred with the AI assistant: ${error.message}`);
    } finally {
      dom.aiAssistBtn.textContent = "✨";
      dom.aiAssistBtn.disabled = false;
    }
  };

  // --- UTILITY FUNCTIONS ---
  function debounce(func, delay) {
    let timeout;
    return function (...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), delay);
    };
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function loadSettings() {
    const settings = JSON.parse(localStorage.getItem("aiSettings"));
    if (settings) {
      dom.apiUrlInput.value = settings.apiUrl || "";
      dom.apiKeyInput.value = settings.apiKey || "";
      dom.modelNameInput.value = settings.modelName || "";
    }
  }

  // --- INITIALIZATION ---
  const init = async () => {
    // Attach event listeners
    dom.newNoteBtn.addEventListener("click", handleNewNote);
    dom.notesList.addEventListener("click", handleNoteSelection);
    dom.noteTitle.addEventListener("input", debouncedUpdate);
    dom.noteContent.addEventListener("input", debouncedUpdate);
    dom.settingsBtn.addEventListener("click", () => handleSettingsToggle(true));
    dom.closeModalBtn.addEventListener("click", () =>
      handleSettingsToggle(false),
    );
    dom.saveSettingsBtn.addEventListener("click", handleSaveSettings);
    dom.aiAssistBtn.addEventListener("click", handleAiAssist);

    // Close modal if clicked outside
    dom.settingsModal.addEventListener("click", (e) => {
      if (e.target === dom.settingsModal) {
        handleSettingsToggle(false);
      }
    });

    // Fetch initial data and render
    try {
      state.notes = await api.getNotes();
      renderNotesList();
      renderEditor();
    } catch (error) {
      console.error("Initialization failed:", error);
      dom.notesList.innerHTML = '<p class="error">Could not load notes.</p>';
    }
  };

  init();
});
