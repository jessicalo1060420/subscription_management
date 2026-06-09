<template>
  <div class="form-page">
    <div class="form">
      <h2>{{ isEditing ? "修改訂閱" : "新增訂閱" }}</h2>

      <div class="form-row">
        <label>*服務名稱</label>
        <input v-model="form.service_name" placeholder="例如：Netflix" />
      </div>

      <div class="form-row">
        <label>方案名稱</label>
        <input v-model="form.plan_name" placeholder="例如：Premium" />
      </div>

      <div class="form-row">
        <label>*類別名稱</label>
        <select v-model.number="form.category_id">
          <option value="1">娛樂</option>
          <option value="2">工作與生產力</option>
          <option value="3">學習教育</option>
          <option value="4">雲端與科技</option>
          <option value="5">生活</option>
          <option value="6">其他</option>
        </select>
      </div>

      <div class="form-row">
        <label>*價格</label>
        <input v-model.number="form.price" />
      </div>

      <div class="form-row">
        <label>扣款週期</label>
        <select v-model="form.billing_cycle">
          <option value="1">日繳</option>
          <option value="7">週繳</option>
          <option value="30">月繳</option>
          <option value="90">季繳</option>
          <option value="180">半年繳</option>
          <option value="365">年繳</option>
        </select>
      </div>

      <div class="form-row">
        <label>*下次扣款日</label>
        <input v-model="form.payment_day" type="date" />
        
      </div>

      

      

      <button @click="$emit('submit-form')">
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
  </div>
</template>

<script>
export default {
  props: {
    form: Object,
    isEditing: Boolean
  },

  emits: ["submit-form", "cancel-edit"]
};
</script>

<style scoped>
.form-page {
  
  display: flex;
  justify-content: center;
  
  background: #f7f7f7;
  padding: 40px 16px;
}

.form {
  width: 420px;
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
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #444;
}

input,
select {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  font-size: 15px;
  background: #fff;
  color: #000;
  outline: none;
}
input[type="date"] {
  color: #000;
  background-color: #fff;
  color-scheme: light;
  cursor: pointer;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 1;
  cursor: pointer;
}
input::placeholder {
  color: #999;
}

input:focus,
select:focus {
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