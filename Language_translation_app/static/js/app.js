/**
 * LinguaAI — Frontend Controller
 * Handles: translation API calls, TTS, copy-to-clipboard,
 *          language swap, quick chips, keyboard shortcuts, toast notifications.
 */

'use strict';

// ─── DOM References ───────────────────────────────────────────────
const sourceText     = document.getElementById('source-text');
const outputArea     = document.getElementById('output-area');
const sourceLang     = document.getElementById('source-lang');
const targetLang     = document.getElementById('target-lang');
const translateBtn   = document.getElementById('translate-btn');
const swapBtn        = document.getElementById('swap-btn');
const clearBtn       = document.getElementById('clear-btn');
const copyBtn        = document.getElementById('copy-btn');
const charCount      = document.getElementById('char-count');
const outputInfo     = document.getElementById('output-info');
const speakSourceBtn = document.getElementById('speak-source-btn');
const speakOutputBtn = document.getElementById('speak-output-btn');
const audioPlayer    = document.getElementById('audio-player');
const toast          = document.getElementById('toast');
const quickChips     = document.querySelectorAll('#quick-chips .chip');

// ─── State ────────────────────────────────────────────────────────
let translatedText   = '';
let currentAudioUrl  = '';
let toastTimer       = null;
let debounceTimer    = null;

// ─── Utility: Show Toast ──────────────────────────────────────────
function showToast(message, type = 'info', duration = 3000) {
  if (toastTimer) clearTimeout(toastTimer);
  toast.textContent = message;
  toast.className = `toast show ${type}`;
  toastTimer = setTimeout(() => {
    toast.className = 'toast';
  }, duration);
}

// ─── Utility: Update character counter ───────────────────────────
function updateCharCount() {
  const len = sourceText.value.length;
  charCount.textContent = `${len.toLocaleString()} / 5,000`;
  charCount.style.color = len > 4500 ? 'var(--clr-error)' : 'var(--clr-text-3)';
}

// ─── Translate ────────────────────────────────────────────────────
async function performTranslation() {
  const text = sourceText.value.trim();
  if (!text) {
    showToast('⚠️ Please enter text to translate.', 'error');
    sourceText.focus();
    return;
  }

  const src = sourceLang.value;
  const tgt = targetLang.value;

  if (src !== 'auto' && src === tgt) {
    showToast('⚠️ Source and target languages are the same.', 'error');
    return;
  }

  // UI: loading state
  translateBtn.classList.add('loading');
  translateBtn.disabled = true;
  outputArea.classList.add('loading');
  outputArea.innerHTML = '';
  copyBtn.disabled = true;
  speakOutputBtn.disabled = true;

  try {
    const response = await fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, source_lang: src, target_lang: tgt }),
    });

    const data = await response.json();

    if (data.success) {
      translatedText = data.translated_text;
      outputArea.textContent = translatedText;
      outputInfo.textContent = `${translatedText.length.toLocaleString()} chars`;
      copyBtn.disabled = false;
      speakOutputBtn.disabled = false;
      showToast('✅ Translation complete!', 'success');
    } else {
      outputArea.innerHTML = `<span style="color:var(--clr-error)">${data.error}</span>`;
      showToast(`❌ ${data.error}`, 'error');
    }
  } catch (err) {
    outputArea.innerHTML = `<span style="color:var(--clr-error)">Network error. Please try again.</span>`;
    showToast('❌ Network error. Check your connection.', 'error');
    console.error('Translation error:', err);
  } finally {
    translateBtn.classList.remove('loading');
    translateBtn.disabled = false;
    outputArea.classList.remove('loading');
  }
}

// ─── Text-to-Speech ───────────────────────────────────────────────
async function speakText(text, langCode, btn) {
  if (!text.trim()) {
    showToast('⚠️ No text to speak.', 'error');
    return;
  }

  // If already playing this audio, pause it
  if (btn.classList.contains('speaking')) {
    audioPlayer.pause();
    btn.classList.remove('speaking');
    return;
  }

  btn.classList.add('speaking');
  btn.disabled = true;

  try {
    const response = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, lang: langCode }),
    });

    const data = await response.json();

    if (data.success) {
      audioPlayer.src = data.audio_url;
      audioPlayer.play();
      audioPlayer.onended = () => {
        btn.classList.remove('speaking');
        btn.disabled = false;
      };
    } else {
      showToast(`❌ TTS failed: ${data.error}`, 'error');
      btn.classList.remove('speaking');
    }
  } catch (err) {
    showToast('❌ Network error during TTS.', 'error');
    btn.classList.remove('speaking');
    console.error('TTS error:', err);
  } finally {
    btn.disabled = false;
  }
}

// ─── Copy to Clipboard ────────────────────────────────────────────
async function copyTranslation() {
  if (!translatedText) return;

  try {
    await navigator.clipboard.writeText(translatedText);
    copyBtn.classList.add('copied');
    const originalContent = copyBtn.innerHTML;
    copyBtn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      Copied!
    `;
    showToast('📋 Copied to clipboard!', 'success', 2000);
    setTimeout(() => {
      copyBtn.classList.remove('copied');
      copyBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
        </svg>
        Copy
      `;
    }, 2000);
  } catch {
    // Fallback for older browsers
    const el = document.createElement('textarea');
    el.value = translatedText;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    showToast('📋 Copied!', 'success', 2000);
  }
}

// ─── Swap Languages ───────────────────────────────────────────────
function swapLanguages() {
  const srcVal = sourceLang.value;
  const tgtVal = targetLang.value;

  // Don't swap if source is "auto"
  if (srcVal === 'auto') {
    showToast('ℹ️ Set a specific source language to swap.', 'info');
    return;
  }

  // Find matching option in source select for the target value
  const srcOption = [...sourceLang.options].find(o => o.value === tgtVal);
  const tgtOption = [...targetLang.options].find(o => o.value === srcVal);

  if (srcOption && tgtOption) {
    sourceLang.value = tgtVal;
    targetLang.value = srcVal;

    // Also swap text content
    const currentSource = sourceText.value;
    const currentOutput = translatedText;
    if (currentOutput) {
      sourceText.value = currentOutput;
      translatedText = currentSource;
      outputArea.textContent = currentSource || '';
      outputArea.querySelector && (outputArea.innerHTML = currentSource
        ? currentSource
        : '<span class="placeholder-text">Your translation will appear here…</span>'
      );
      updateCharCount();
    }
    showToast('🔄 Languages swapped!', 'success', 1500);
  }
}

// ─── Quick Language Chips ─────────────────────────────────────────
quickChips.forEach(chip => {
  chip.addEventListener('click', () => {
    const lang = chip.dataset.lang;

    // Set target language
    const option = [...targetLang.options].find(o => o.value === lang);
    if (option) {
      targetLang.value = lang;
    }

    // Update active chip
    quickChips.forEach(c => c.classList.remove('active'));
    chip.classList.add('active');

    // Auto-translate if there's existing text
    if (sourceText.value.trim()) {
      performTranslation();
    }
  });
});

// ─── Event Listeners ──────────────────────────────────────────────
translateBtn.addEventListener('click', performTranslation);

clearBtn.addEventListener('click', () => {
  sourceText.value = '';
  updateCharCount();
  outputArea.innerHTML = '<span class="placeholder-text">Your translation will appear here…</span>';
  outputInfo.textContent = '';
  translatedText = '';
  copyBtn.disabled = true;
  speakOutputBtn.disabled = true;
  sourceText.focus();
});

copyBtn.addEventListener('click', copyTranslation);

swapBtn.addEventListener('click', swapLanguages);

speakSourceBtn.addEventListener('click', () => {
  const text = sourceText.value.trim();
  const lang = sourceLang.value === 'auto' ? 'en' : sourceLang.value;
  speakText(text, lang, speakSourceBtn);
});

speakOutputBtn.addEventListener('click', () => {
  speakText(translatedText, targetLang.value, speakOutputBtn);
});

// Stop audio on pause/ended
audioPlayer.addEventListener('pause', () => {
  document.querySelectorAll('.tts-btn.speaking').forEach(btn => {
    btn.classList.remove('speaking');
  });
});

// Character counter with debounced auto-translate
sourceText.addEventListener('input', () => {
  updateCharCount();

  // Debounce auto-translate (2 seconds after stop typing)
  clearTimeout(debounceTimer);
  if (sourceText.value.trim().length > 10) {
    debounceTimer = setTimeout(performTranslation, 2000);
  }
});

// Keyboard shortcut: Ctrl+Enter or Cmd+Enter
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    clearTimeout(debounceTimer);
    performTranslation();
  }
  // Escape key clears text
  if (e.key === 'Escape' && document.activeElement === sourceText) {
    clearBtn.click();
  }
});

// ─── Init ─────────────────────────────────────────────────────────
updateCharCount();
