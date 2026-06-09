

<template>
  <div class="page">
    <h1>訂閱管理系統</h1>

    <div v-if="!currentUser">
      <LoginForm
        v-if="currentPage === 'login'"
        :loginForm="loginForm"
        @login="login"
        @go-register="currentPage = 'register'"
      />

      <RegisterForm
        v-if="currentPage === 'register'"
        :registerForm="registerForm"
        @register="register"
        @go-login="currentPage = 'login'"
      />
    </div>

    <div v-else>
      <div class="top-bar">
        <div class="user-info">
          <span>目前使用者</span>
          <strong>{{ currentUser.user_name }}</strong>
        </div>

        <div class="nav-buttons">
          <button @click="currentPage = 'form'">新增訂閱</button>
          <button @click="currentPage = 'list'">訂閱清單</button>
          <button class="cancel" @click="logout">登出</button>
        </div>
      </div>
      <SubscriptionForm
        v-if="currentPage === 'form'"
        :form="form"
        :isEditing="isEditing"
        @submit-form="submitForm"
        @cancel-edit="cancelEdit"
      />

      <SubscriptionList
        v-if="currentPage === 'list'"
        :subscriptions="subscriptions"
        :sortedSubscriptions="sortedSubscriptions"
        :totalPrice="totalPrice"
        :sortBy="sortBy"
        @update-sort="sortBy = $event"
        @edit-item="editItem"
        @delete-item="deleteItem"
      />
    </div>
  </div>
</template>
<script>
import SubscriptionForm from "./components/SubscriptionForm.vue";
import SubscriptionList from "./components/SubscriptionList.vue";
import LoginForm from "./components/LoginForm.vue";
import RegisterForm from "./components/RegisterForm.vue";
const API_URL = "http://127.0.0.1:5000";

export default {
  data() {
    return {
      currentPage: "login",
      currentUser: null,

      loginForm: {
        user_name: "",
        user_password: ""
      },

      registerForm: {
        user_name: "",
        user_email: "",
        user_password: ""
      },
      subscriptions: [],
      isEditing: false,
      editingId: null,
      sortBy: "newest",
      

      form: {
        user_id: null,
        category_id: 1,
        service_name: "",
        plan_name: "",
        price: null,
        billing_cycle: 30,
        payment_day: ""
        
      }
    };
  },

  computed: {
    totalPrice() {
      const total = this.subscriptions.reduce((sum, item) => {
        const price = Number(item.price || 0);
        const cycle = Number(item.billing_cycle || 1);

        return sum + price * (30 / cycle);
      }, 0);

      return Math.round(total);
    },
    sortedSubscriptions() {
    const list = [...this.subscriptions];

    switch (this.sortBy) {
      case "newest":
        return list.sort((a, b) => b.subscription_id - a.subscription_id);

      case "oldest":
        return list.sort((a, b) => a.subscription_id - b.subscription_id);

      case "category":
        return list.sort((a, b) =>
          (a.category_name || "").localeCompare(b.category_name || "")
        );

      case "payment":
        return list.sort((a, b) =>
          (a.payment_day || 99) - (b.payment_day || 99)
        );

      default:
        return list;
    }
  }
  },
  
  components: {
    SubscriptionForm,
    SubscriptionList,
    LoginForm,
    RegisterForm
  },

  
  mounted() {
    if (this.currentUser) {
      this.getSubscriptions();
    }
  },

  methods: {
    async getSubscriptions() {
      if (!this.currentUser) {
        return;
      }
      const res = await fetch(`${API_URL}/subscriptions/${this.currentUser.user_id}`);
      this.subscriptions = await res.json();
    },
    async login() {
      const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.loginForm)
      });

      const data = await res.json();

      if (res.ok) {
        this.currentUser = data;
        this.form.user_id = data.user_id;
        this.currentPage = "list";
        this.getSubscriptions();
      } else {
        alert(data.message);
      }
    },
    async register() {
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.registerForm)
      });

      const data = await res.json();

      if (res.ok) {
        alert("註冊成功，請登入");
        this.currentPage = "login";
      } else {
        alert("註冊失敗");
      }
    },
    async submitForm() {
      if (!this.currentUser) {
        alert("請先登入");
        this.currentPage = "login";
        return;
      }
      this.form.user_id = this.currentUser.user_id;
      if (this.isEditing) {
        await fetch(`${API_URL}/subscriptions/${this.editingId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(this.form)
        });
      } else {
        await fetch(`${API_URL}/subscriptions`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(this.form)
        });
      }

      this.resetForm();
      this.getSubscriptions();
      this.currentPage = "list";
    },
    logout() {
      this.currentUser = null;
      this.currentPage = "login";
      this.subscriptions = [];
      this.resetForm();
    },
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.subscription_id;

      this.form = {
        user_id: this.currentUser.user_id,
        category_id: 1,
        service_name: item.service_name,
        plan_name: item.plan_name,
        price: item.price,
        billing_cycle: item.billing_cycle,
        payment_day: item.payment_day
      };
      this.currentPage = "form";
    },

    async deleteItem(id) {
      if (confirm("確定要刪除這筆訂閱嗎？")) {
        await fetch(`${API_URL}/subscriptions/${id}`, {
          method: "DELETE"
        });

        this.getSubscriptions();
      }
    },

    cancelEdit() {
      this.resetForm();
    },

    resetForm() {
      this.isEditing = false;
      this.editingId = null;

      this.form = {
        user_id: this.currentUser ? this.currentUser.user_id : null,
        category_id: 1,
        service_name: "",
        plan_name: "",
        price: null,
        billing_cycle: 30,
        payment_day: null
      };
    }
  }
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, "Microsoft JhengHei", sans-serif;
  background: #f7f7f7;
  color: #222;
}

.page {
  max-width: 1100px;
  margin: 0px auto;
  padding: 24px;
}

h1 {
  text-align: center;
  font-size: 28px;
  font-weight: 500;
  color: #222;
  margin-bottom: 32px;
}

h2 {
  text-align: center;
  font-size: 22px;
  font-weight: 500;
  color: #222;
}

p {
  color: #333;
}

.summary {
  display: flex;
  gap: 16px;
  margin: 24px 0;
}

.summary p {
  flex: 1;
  margin: 0;
  padding: 20px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  box-shadow: none;
}

.form {
  background: #fff;
  padding: 32px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: none;
}

input,
select {
  display: block;
  width: 100%;
  padding: 10px 12px;
  margin: 8px 0;
  box-sizing: border-box;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  background: #fff;
  color: #000;
  outline: none;
}

input::placeholder {
  color: #999;
}

input:focus,
select:focus {
  border-color: #888;
}

button {
  padding: 9px 14px;
  margin: 4px;
  border: 1px solid #222;
  border-radius: 8px;
  background: #222;
  color: #fff;
  cursor: pointer;
}

.cancel,
.delete {
  background: #fff;
  color: #222;
}

button:hover {
  opacity: 0.85;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: none;
}

th,
td {
  padding: 14px 12px;
  border-bottom: 1px solid #eee;
  text-align: center;
  color: #222;
}

th {
  background: #f7f7f7;
  color: #333;
  font-weight: 500;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 14px;
}

.form-row label {
  width: 120px;
  font-weight: 400;
  color: #444;
}

.form-row input,
.form-row select {
  flex: 1;
}

.chart-box {
  background: #fff;
  padding: 28px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  margin: 24px 0;
  max-width: 500px;
  box-shadow: none;
}
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e5e5;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-info span {
  font-size: 13px;
  color: #777;
}

.user-info strong {
  font-size: 18px;
  font-weight: 500;
  color: #222;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.nav-buttons button {
  margin: 0;
}
</style>