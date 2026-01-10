<template>
  <div class="upload-wrapper">
    <!-- Dropzone -->
    <div
      class="dropzone"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="triggerFileSelect"
    >
      <div v-if="!uploading" class="dropzone-content">
        <div class="upload-icon">⬆</div>
        <p class="dropzone-title">Upload Document</p>
        <p class="dropzone-subtitle">Click or drag and drop your file here</p>
        <p class="dropzone-formats">Supported formats: PDF, JPG, PNG, TXT (max 12 MB)</p>
      </div>
      <p v-else class="dropzone-loading">Processing analysis...</p>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      accept=".pdf, .png, .jpg, .jpeg, .txt"
      class="hidden-input"
      @change="handleFileSelect"
    />

    <!-- Progress Bar -->
    <div v-if="uploading" class="progress-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { toast } from 'vue-sonner'

const fileInput = ref(null)
const uploading = ref(false)
const progress = ref(0)

const emit = defineEmits(['analysis-result', 'analysis-started'])

/* -------------------------------------------------------------------------- */
/* Trigger file select                                                        */
/* -------------------------------------------------------------------------- */
function triggerFileSelect() {
  fileInput.value?.click()
}

/* -------------------------------------------------------------------------- */
/* Handle drop                                                                */
/* -------------------------------------------------------------------------- */
function handleDrop(event) {
  const file = event.dataTransfer.files[0]
  validateAndUpload(file)
}

/* -------------------------------------------------------------------------- */
/* Handle file selection                                                      */
/* -------------------------------------------------------------------------- */
function handleFileSelect(event) {
  const file = event.target.files[0]
  validateAndUpload(file)
}

/* -------------------------------------------------------------------------- */
/* Validate file before upload                                                */
/* -------------------------------------------------------------------------- */
function validateAndUpload(file) {
  if (!file) return

  const allowed = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
  if (!allowed.includes(file.type)) {
    toast.error('Invalid file type. Allowed formats: PDF, JPG, PNG, TXT.')
    return
  }

  if (file.size > 12 * 1024 * 1024) {
    toast.error('File size exceeds limit. Maximum file size: 12 MB.')
    return
  }

  // Get file extension
  const fileExt = file.name.split('.').pop().toUpperCase()
  
  // Emit with file info
  emit('analysis-started', {
    fileName: file.name,
    fileType: fileExt
  })
  
  uploadFile(file)
}

/* -------------------------------------------------------------------------- */
/* Upload + Backend Request                                                   */
/* -------------------------------------------------------------------------- */
async function uploadFile(file) {
  uploading.value = true
  progress.value = 10

  toast.info('Uploading document...', {
    description: `${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`,
  })

  // Create an AbortController for timeout
  const controller = new AbortController()
  const timeoutId = setTimeout(() => {
    controller.abort()
  }, 120000) // 120 seconds timeout (2 minutes)

  try {
    const formData = new FormData()
    formData.append('file', file)

    progress.value = 30

    console.log('Sending request to backend...')
    
    const response = await fetch(
      'http://127.0.0.1:8000/upload',
      {
        method: 'POST',
        body: formData,
        signal: controller.signal, // Add abort signal
      },
    )

    clearTimeout(timeoutId) // Clear timeout on success
    progress.value = 60

    console.log('Response received:', response.status)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Backend error response:', errorText)
      toast.error('Backend analysis error.')
      throw new Error(`Server error: ${response.status}`)
    }

    const data = await response.json()
    console.log('Data received:', data)
    progress.value = 100

    emit('analysis-result', data)
  } catch (err) {
    clearTimeout(timeoutId) // Clear timeout on error
    
    let errorMessage = err.message
    
    if (err.name === 'AbortError') {
      errorMessage = 'Request timeout. The backend took too long to respond (>2 minutes). Please check if the backend is running and the OpenAI API key is valid.'
      console.error('Request timeout after 120 seconds')
    } else if (err.message.includes('Failed to fetch')) {
      errorMessage = 'Cannot connect to backend. Make sure the backend server is running on http://127.0.0.1:8000'
      console.error('Backend connection failed')
    }
    
    console.error('Upload error:', err)
    
    toast.error('Upload failed.', {
      description: errorMessage,
      duration: 8000,
    })
    emit('analysis-result', {
      error: `Upload failed: ${errorMessage}`,
    })
  } finally {
    setTimeout(() => {
      uploading.value = false
      progress.value = 0
    }, 1000)
  }
}
</script>

<style scoped>
.upload-wrapper {
  width: 100%;
  max-width: 600px;
  margin: 0 auto 2rem;
}

.dropzone {
  border: 2px dashed #cbd5e1;
  border-radius: 0.5rem;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  background: #ffffff;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.dropzone:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  transform: translateY(-2px);
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.upload-icon {
  font-size: 3rem;
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.dropzone-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e3a5f;
  margin: 0;
}

.dropzone-subtitle {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
  font-weight: 500;
}

.dropzone-formats {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: 0.5rem 0 0 0;
  font-weight: 400;
}

.dropzone-loading {
  font-size: 1rem;
  color: #2c5f8d;
  font-weight: 600;
  margin: 0;
}

.hidden-input {
  display: none;
}

.progress-container {
  width: 100%;
  background: #e2e8f0;
  height: 6px;
  border-radius: 3px;
  margin-top: 1rem;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #2c5f8d 0%, #3b82f6 100%);
  transition: width 0.3s ease;
  box-shadow: 0 1px 2px rgba(59, 130, 246, 0.3);
}
</style>
