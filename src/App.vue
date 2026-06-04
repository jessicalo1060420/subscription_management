<template>
  <div class="page">
    <h1>訂閱服務與扣款管理系統</h1>

    <div class="form">
  <h2>{{ isEditing ? "修改訂閱" : "新增訂閱" }}</h2>

  <div class="form-row">
    <label>*服務名稱</label>
    <input v-model="form.service_name" placeholder="例如：Netflix" />
  </div>

  <div class="form-row">
    <label>*方案名稱</label>
    <input v-model="form.plan_name" placeholder="例如：Premium" />
  </div>

  <div class="form-row">
    <label>*類別名稱</label>
    <select v-model.number="form.category_id">
      <option value="1">影音</option>
      <option value="2">音樂</option>
      <option value="3">雲端</option>
      <option value="4">AI工具</option>
    </select>
  </div>

  <div class="form-row">
    <label>*價格</label>
    <input v-model.number="form.price" />
  </div>

  <div class="form-row">
    <label>扣款週期</label>
    <input v-model.number="form.billing_cycle" placeholder="每週＝7;每月＝30;每年＝365 "/>
  </div>

  <div class="form-row">
    <label>*扣款日期</label>
    <input v-model.number="form.payment_day" type="date"/>
  </div>

  <div class="form-row">
    <label>開始日期</label>
    <input v-model="form.start_date" type="date" />
  </div>

  <div class="form-row">
    <label>*狀態</label>
    <select v-model="form.status">
      <option value="已付款">已付款</option>
      <option value="未付款">未付款</option>
      <option value="已停止">已停止</option>
    </select>
  </div>

  <button @click="submitForm">
    {{ isEditing ? "儲存修改" : "新增" }}
  </button>

  <button
    v-if="isEditing"
    class="cancel"
    @click="cancelEdit"
  >
    取消修改
  </button>
  
</div>
<div class="summary">
      <p>訂閱數量：{{ subscriptions.length }}</p>
      <p>每月總金額：約 NT$ {{ totalPrice }}</p>
</div>
    <h2>訂閱清單</h2>

    <table>
      <thead>
        <tr>
          <th>服務</th>
          <th>方案</th>
          <th>類別</th>
          <th>價格</th>
          <th>週期</th>
          <th>扣款日</th>
          <th>狀態</th>
          <th>開始日期</th>
          <th>操作</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in subscriptions" :key="item.subscription_id">
          <td>{{ item.service_name }}</td>
          <td>{{ item.plan_name }}</td>
          <td>{{ item.category_name }}</td>
          <td>NT$ {{ item.price }}</td>
          <td>{{ item.billing_cycle }} 天</td>
          <td>每月 {{ item.payment_day }} 號</td>
          <td>{{ item.status }}</td>
          <td>{{ item.start_date }}</td>
          <td>
            <button @click="editItem(item)">修改</button>
            <button class="delete" @click="deleteItem(item.subscription_id)">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
const API_URL = "http://127.0.0.1:5000";

export default {
  data() {
    return {
      subscriptions: [],
      isEditing: false,
      editingId: null,
      form: {
        user_id: 1,
        category_id: 1,
        service_name: "",
        plan_name: "",
        status: "已付款",
        start_date: "",
        price: null,
        billing_cycle: null,
        payment_day: ""
      }
    };
  },

  computed: {
    totalPrice() {
      return this.subscriptions.reduce((sum, item) => {
        return sum + Number(item.price || 0);
      }, 0);
    }
  },

  mounted() {
    this.getSubscriptions();
  },

  methods: {
    async getSubscriptions() {
      const res = await fetch(`${API_URL}/subscriptions`);
      this.subscriptions = await res.json();
    },

    async submitForm() {
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
    },

    editItem(item) {
      this.isEditing = true;
      this.editingId = item.subscription_id;

      this.form = {
        user_id: 1,
        category_id: 1,
        service_name: item.service_name,
        plan_name: item.plan_name,
        status: item.status,
        start_date: item.start_date,
        price: item.price,
        billing_cycle: item.billing_cycle,
        payment_day: item.payment_day
      };
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
        user_id: 1,
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
</style>