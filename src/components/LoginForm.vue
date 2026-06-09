<template>
  <div class="login-page">
    <div class="form">
      <h2>登入</h2>

      <div class="form-row">
        <label>使用者名稱</label>
        <input
          v-model="loginForm.user_name"
          type="name"
          placeholder="請輸入使用者名稱"
        />
      </div>

      <div class="form-row">
        <label>密碼</label>
        <input
          v-model="loginForm.user_password"
          type="password"
          placeholder="請輸入密碼"
        />
      </div>

      <button @click="$emit('login')">登入</button>

      <button class="cancel" @click="$emit('go-register')">
        前往註冊
      </button>
    </div>
  </div>
</template>

<script> 
export default {
  props: {
    loginForm: Object
  },

  emits: ["login", "go-register"]
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 40px;
  background: #f7f7f7;
}

.form {
  width: 360px;
  padding: 40px;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
}

h2 {
  margin-bottom: 32px;
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  color: #222;
}

.form-row {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #444;
}

input {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  font-size: 15px;
  background: #fff;
  outline: none;
  color: #000;
}

input:focus {
  border-color: #888;
}

button {
  width: 100%;
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #222;
  border-radius: 8px;
  background: #222;
  color: #fff;
  font-size: 15px;
  cursor: pointer;
}

.cancel {
  background: #fff;
  color: #222;
}

button:hover {
  opacity: 0.85;
}
</style>