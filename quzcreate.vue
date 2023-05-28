<template>
  <div id="app">
    <h1>問題集生成アプリケーション</h1>
    <textarea v-model="textInput" placeholder="テキストを入力してください"></textarea>
    <input v-model="questionNumber" type="number" placeholder="問題数を入力してください">
    <input v-model="apiKey" type="text" placeholder="APIキーを入力してください">
    <button @click="generateQuestions">問題生成</button>
    <div v-for="(item, index) in questions" :key="index">
      <p>{{ item.question }}</p>
      <p>{{ item.answer }}</p>
    </div>
    <button @click="downloadCSV">CSVダウンロード</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      textInput: '',
      questionNumber: '',
      apiKey: '',
      questions: []
    }
  },
  methods: {
    async generateQuestions() {
      const response = await axios.post('/api/generate-questions', {
        text_input: this.textInput,
        number_input: this.questionNumber,
        API_KEY_input: this.apiKey
      })
      this.questions = response.data.questions
    },
    downloadCSV() {
      window.open('/api/download-csv')
    }
  }
}
</script>
