<template>
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