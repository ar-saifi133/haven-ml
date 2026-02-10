# Adding Video to GitHub README

## Method 1: GitHub-Hosted Video (Recommended) ⭐

**Best for**: Videos under 10MB

### Steps:
1. **Record your demo video** (MP4, MOV, or WEBM)
2. **Compress if needed**:
   ```bash
   # Using ffmpeg to compress
   ffmpeg -i input.mp4 -vcodec h264 -acodec aac demo.mp4
   ```
3. **Upload to GitHub**:
   - Go to any GitHub issue or PR in your repo
   - Drag & drop your video file
   - GitHub will upload it and give you a URL like:
     ```
     https://user-images.githubusercontent.com/123456789/video-id.mp4
     ```
4. **Add to README**:
   ```markdown
   https://user-images.githubusercontent.com/YOUR_ID/YOUR_VIDEO.mp4
   ```

**Pros**: Direct embedding, no external dependencies  
**Cons**: 10MB limit per file

---

## Method 2: YouTube Video (Best for longer videos)

### Steps:
1. **Upload video to YouTube**
2. **Get video ID** from URL (e.g., `dQw4w9WgXcQ` from `youtube.com/watch?v=dQw4w9WgXcQ`)
3. **Add to README**:
   ```markdown
   [![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
   ```

**Example**:
```markdown
[![Empathy System Demo](https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
```

**Pros**: No size limit, professional hosting  
**Cons**: Requires YouTube account, extra click to watch

---

## Method 3: Animated GIF (Best Compatibility)

### Steps:
1. **Convert video to GIF**:
   
   **Option A - Online** (easiest):
   - Upload to https://ezgif.com/video-to-gif
   - Set size: 800px width max
   - Set FPS: 10-15
   - Download
   
   **Option B - FFmpeg**:
   ```bash
   ffmpeg -i demo.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" -loop 0 demo.gif
   ```

2. **Optimize GIF** (if > 5MB):
   - Use https://ezgif.com/optimize
   - Or: `gifsicle -O3 --colors 256 input.gif > output.gif`

3. **Add to repo**:
   ```bash
   mkdir -p docs
   cp demo.gif docs/
   git add docs/demo.gif
   git commit -m "Add demo GIF"
   git push
   ```

4. **Add to README**:
   ```markdown
   ![Empathy System Demo](docs/demo.gif)
   ```

**Pros**: Works everywhere, auto-plays  
**Cons**: Large file size, lower quality

---

## Method 4: HTML5 Video Tag

For more control, use HTML:

```html
<video width="100%" controls>
  <source src="https://user-images.githubusercontent.com/YOUR_ID/video.mp4" type="video/mp4">
  Your browser doesn't support video.
</video>
```

**Note**: GitHub sanitizes HTML, so this may not work in all cases.

---

## Recommended Approach for Your Project

**Create a 2-tiered approach**:

1. **GIF preview** (10-15 seconds) - Shows in README
2. **Full video link** - Links to YouTube for complete demo

### Example:

```markdown
## 🎬 Demo

![Quick Demo](docs/demo.gif)

**[▶️ Watch Full Demo (4:50)](https://youtu.be/YOUR_VIDEO_ID)** - Complete walkthrough with all features

### Quick Preview
- Real-time face emotion detection
- Voice transcription and analysis
- Multimodal fusion in action
- AI-generated empathetic responses
```

---

## Creating the Demo Video

### What to Include (30-60 seconds GIF):
1. **Opening** (3s): Title screen
2. **Face Detection** (10s): Show different emotions
3. **Voice Analysis** (10s): Speak and show transcription
4. **Fusion** (5s): Show masking detection
5. **Response** (5s): AI response appears
6. **Closing** (2s): Logo/GitHub link

### Tools for Recording:

**Windows**:
- Built-in: Windows + G (Game Bar)
- Professional: OBS Studio (free)

**Screen Recording**:
```bash
# Using OBS Studio
1. Add Display Capture
2. Set output to 1920x1080
3. Record to MP4
```

### Quick Video Creation:

```bash
# 1. Record your screen (30-60 seconds)
# 2. Convert to optimized GIF
ffmpeg -i recording.mp4 -vf "fps=10,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" demo.gif

# 3. Add to repo
git add docs/demo.gif
git commit -m "Add demo GIF to README"
git push
```

---

## Current README Update

I've updated your README with **all 4 options commented out**. 

**Choose one method**:
1. Uncomment your preferred method
2. Replace placeholders with actual video/GIF
3. Commit and push

**My recommendation**: 
- **GIF** for immediate visual impact
- **+ YouTube link** for full demo

This gives users:
- Instant preview (GIF auto-plays)
- Option to watch full video (YouTube link)
- Professional presentation
