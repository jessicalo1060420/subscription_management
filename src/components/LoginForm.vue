<template>
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
</template>

<script> 
export default {
  props: {
    loginForm: Object
  },

  emits: ["login", "go-register"]
  

};
</script>