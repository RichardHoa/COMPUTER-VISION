/**
 * Sets the camera source URL/IP and starts the stream.
 * @param {number} cam_id - Camera ID (1 or 2).
 */
async function setSource(cam_id) {
  const vid = document.getElementById(`video-${cam_id}`);
  const src = document.getElementById(`src-${cam_id}`).value.trim();
  if (!src) {
    alert("Nhập IP/URL camera trước khi Connect (hoặc bấm Stop để dừng).");
    return;
  }
  const res = await fetch('/set_source', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cam_id: cam_id, source: src })
  });
  const j = await res.json();
  if (!j.ok) {
    alert("Lỗi khi connect: " + (j.error || 'unknown'));
    return;
  }
  // Reload the img to pick new stream (cache buster added)
  vid.src = `/video_feed/${cam_id}?t=${Date.now()}`;
}

/**
 * Stops the camera stream.
 * @param {number} cam_id - Camera ID (1 or 2).
 */
async function stopSource(cam_id) {
  const res = await fetch('/set_source', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cam_id: cam_id, source: '' })
  });
  const j = await res.json();
  if (!j.ok) {
    alert("Lỗi khi stop: " + (j.error || 'unknown'));
    return;
  }
  const vid = document.getElementById(`video-${cam_id}`);
  setPlaceholder(vid);
}

/**
 * Captures an image from the specified camera.
 * @param {number} cam_id - The ID of the camera (1 or 2).
 * @param {boolean} [isManual=false] - Whether triggered manually (batch mode) or via click event.
 * @returns {Promise<boolean>} - True if capture successful, false otherwise.
 */
async function capture(cam_id, isManual = false) {
  // Disable button to prevent double-click if triggered via event
  let btn = null;
  if (!isManual && typeof event !== 'undefined') {
    btn = event.currentTarget;
    if (btn) btn.disabled = true;
  }

  try {
    // Get selected filter
    const filterSelect = document.getElementById(`filterSelect-${cam_id}`);
    const step = filterSelect ? filterSelect.value : 'all';

    // Send capture request
    const res = await fetch('/capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cam_id: cam_id, step: step })
    });

    const j = await res.json();
    if (!j.ok) {
      const errMsg = "Capture failed: " + (j.error || 'unknown');
      if (!isManual) alert(errMsg);
      return false;
    }

    // Update DOM with captured and processed images
    const capImg = document.getElementById(`captured-${cam_id}`);
    const fragImg = document.getElementById(`fragment-${cam_id}`);
    if (capImg) capImg.src = j.image;
    if (fragImg) fragImg.src = j.processed;

    // Update process time display
    const timeBox = document.getElementById(`proc-time-${cam_id}`);
    if (timeBox && typeof j.process_time_ms === 'number') {
      timeBox.textContent = `Process time: ${j.process_time_ms.toFixed(2)} ms`;
    }
    return true;
  } catch (err) {
    if (!isManual) alert("Error: " + err);
    return false;
  } finally {
    if (btn) btn.disabled = false;
  }
}

// --- UI helpers ---
// Static inline SVGs for gray placeholders.
const PLACEHOLDER_CAM = 'data:image/svg+xml;base64,' + btoa(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">`
  + `<rect width="640" height="360" fill="#d3d7dd"/>`
  + `<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"`
  + ` font-family="Arial, sans-serif" font-size="32" fill="#666">No Cam</text>`
  + `</svg>`
);

const PLACEHOLDER_IMG = 'data:image/svg+xml;base64,' + btoa(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">`
  + `<rect width="640" height="360" fill="#e7eaef"/>`
  + `<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"`
  + ` font-family="Arial, sans-serif" font-size="28" fill="#777">No Image</text>`
  + `</svg>`
);

function setPlaceholderCam(imgEl) {
  imgEl.src = PLACEHOLDER_CAM;
}

function setPlaceholderImage(imgEl) {
  imgEl.src = PLACEHOLDER_IMG;
}

// Initialize placeholders on page load so UI never collapses or shows broken images.
document.addEventListener('DOMContentLoaded', () => {
  [1, 2].forEach(id => {
    const vid = document.getElementById(`video-${id}`);
    if (vid) {
      setPlaceholderCam(vid);
    }
    const cap = document.getElementById(`captured-${id}`);
    if (cap) {
      setPlaceholderImage(cap);
    }
    const frag = document.getElementById(`fragment-${id}`);
    if (frag) {
      setPlaceholderImage(frag);
    }
  });
});

// --- Batch Test ---
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Runs a batch test: 10 iterations of triggering both cameras, 
 * then taking a full page screenshot and saving it to the server.
 */
async function runBatchTest() {
  const btn = document.getElementById('batch-btn');
  if (btn) btn.disabled = true;

  try {
    for (let i = 0; i < 10; i++) {
      // 1. Trigger Capture for both cameras and wait for completion
      await Promise.all([
        capture(1, true),
        capture(2, true)
      ]);

      // 2. Wait for images to render
      await sleep(2000);

      // DOM manipulation: Temporarily replace MJPEG streams with static placeholders
      // to prevent html2canvas from hanging on infinite streams.
      const vid1 = document.getElementById('video-1');
      const vid2 = document.getElementById('video-2');
      const src1 = vid1 ? vid1.src : '';
      const src2 = vid2 ? vid2.src : '';

      if (vid1) vid1.src = PLACEHOLDER_CAM;
      if (vid2) vid2.src = PLACEHOLDER_CAM;

      // Small delay to allow DOM to update source
      await sleep(400);

      // 3. Take Screenshot using html2canvas
      let canvas;
      try {
        const screenshotPromise = html2canvas(document.body, {
          useCORS: true,
          logging: false,
          scale: 1
        });

        // Timeout fallback (5s) to avoid infinite hanging
        const timeoutPromise = new Promise((_, reject) =>
          setTimeout(() => reject(new Error("html2canvas timeout")), 5000)
        );

        canvas = await Promise.race([screenshotPromise, timeoutPromise]);
      } catch (err) {
        // Continue to next iteration even if screenshot fails
      }

      // Restore video feeds
      if (vid1) vid1.src = src1;
      if (vid2) vid2.src = src2;

      // 4. Send screenshot to server
      if (canvas) {
        const dataUrl = canvas.toDataURL("image/png");
        await fetch('/save_screenshot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: dataUrl })
        });
      }

      // 5. Wait before next iteration
      await sleep(2000);
    }
    alert("Batch Test Completed!");
  } catch (e) {
    alert("Batch Test Error: " + e);
  } finally {
    if (btn) btn.disabled = false;
  }
}
