

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
      <p>目前使用者：{{ currentUser.user_name }}</p>

      <button @click="currentPage = 'form'">新增訂閱</button>
      <button @click="currentPage = 'list'">訂閱清單</button>
      <button class="cancel" @click="logout">登出</button>

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
        status: "已付款",
        start_date: "",
        price: null,
        billing_cycle: 30,
        payment_day: ""
        
      }
    };
  },

  computed: {
    totalPrice() {
      return this.subscriptions.reduce((sum, item) => {
        const price = Number(item.price || 0);
        const cycle = Number(item.billing_cycle || 1);

        const monthlyPrice = price * (30 / cycle);

        return sum + monthlyPrice;
      }, 0);
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
        status: item.status,
        start_date: item.start_date,
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
        status: "有付",
        start_date: "",
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
  background: #f4f6f8;
}

.page {
  max-width: 1100px;
  margin: 30px auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
}
h2 {
  text-align: center;
  color: #2c3e50;
}

.summary {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.summary p {
  background: white;
  padding: 16px;
  border-radius: 10px;
  flex: 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  
}

input,
select {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  box-sizing: border-box;
}

button {
  padding: 8px 14px;
  margin: 4px;
  border: none;
  border-radius: 6px;
  background: #3498db;
  color: white;
  cursor: pointer;
}

button:hover {
  opacity: 0.85;
}

.delete {
  background: #e74c3c;
}

.cancel {
  background: #7f8c8d;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

th,
td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

th {
  background: #2c3e50;
  color: white;
}
.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.form-row label {
  width: 120px;
  font-weight: bold;
}

.form-row input,
.form-row select {
  flex: 1;
  padding: 8px;
}
.chart-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
  max-width: 500px;
}
</style>