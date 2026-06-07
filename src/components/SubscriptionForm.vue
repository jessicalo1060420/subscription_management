<template>
  <div class="page">

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
    <input v-model="form.payment_day" type="date"/>
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