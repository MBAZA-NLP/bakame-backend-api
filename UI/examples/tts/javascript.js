const text = "Mukomeze mugire ibihe byiza!";

const host = "https://domain.com";
const port = 8000;

const url = host + ":" + port + "/tts";

const data = { text: text };

const options = {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
};

fetch(url, options)
  .then(response => response.arrayBuffer())
  .then(arrayBuffer => {
    const buffer = new Uint8Array(arrayBuffer).buffer;
    const blob = new Blob([buffer], { type: "audio/wav" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "audio.wav";
    link.click();
  });
