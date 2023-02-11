package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"
)

func main() {
	text := "Mukomeze mugire ibihe byiza!"

	host := "https://domain.com"
	port := 8000

	url := host + ":" + string(port) + "/tts"

	data := map[string]string{"text": text}
	jsonData, _ := json.Marshal(data)

	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)

	err := ioutil.WriteFile("audio.wav", body, 0644)
	if err != nil {
		panic(err)
	}
}
