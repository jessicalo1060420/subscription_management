<template>
  <div class="register-page">
    <div class="form">
      <h2>註冊</h2>

      <div class="form-row">
        <label>使用者名稱</label>
        <input
          v-model="registerForm.user_name"
          placeholder="請輸入使用者名稱"
        />
      </div>

      <div class="form-row">
        <label>電子信箱</label>
        <input
          v-model="registerForm.user_email"
          type="email"
          placeholder="請輸入電子信箱"
        />
      </div>

      <div class="form-row">
        <label>密碼</label>
        <input
          v-model="registerForm.user_password"
          type="password"
          placeholder="請輸入密碼"
        />
      </div>

      <button @click="checkRegister">
        註冊
      </button>

      <button class="cancel" @click="$emit('go-login')">
        返回登入
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    registerForm: Object
  },

  emits: ["register", "go-login"],

  methods: {
    checkRegister() {
      if (
        !this.registerForm.user_name?.trim() ||
        !this.registerForm.user_email?.trim() ||
        !this.registerForm.user_password?.trim()
      ) {
        alert("請填寫所有註冊資料");
        return;
      }

      this.$emit("register");
    }
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f7f7f7;
}

.form {
  width: 380px;
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
  border: 1px solid #dcdcdc;
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