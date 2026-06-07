<template>
    <div class="summary">
      <p>訂閱數量：{{ subscriptions.length }}</p>
      <p>每月總金額：約 NT$ {{ totalPrice }}</p>
</div>
<div class="form-row">
  <label>排序方式</label>
  <select 
    value="sortBy"
    @change="$emit('update-sort', $event.target.value)"
    >
    <option value="newest">由新到舊排序</option>
    <option value="oldest">由舊到新排序</option>
    <option value="category">依類別排序</option>
    <option value="payment">依扣款日排序</option>
  </select>
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
        <tr v-for="item in sortedSubscriptions" :key="item.subscription_id">
          <td>{{ item.service_name }}</td>
          <td>{{ item.plan_name }}</td>
          <td>{{ item.category_name }}</td>
          <td>NT$ {{ item.price }}</td>
          <td>{{ item.billing_cycle }} 天</td>
          <td>每月 {{ item.payment_day }} 號</td>
          <td>{{ item.status }}</td>
          <td>{{ item.start_date }}</td>
          <td>
            <button @click="$emit('edit-item', item)">修改</button>
            <button class="delete" @click="$emit('delete-item', item.subscription_id)">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>
  
</template>
<script>
export default {
  props: {
    subscriptions: Array,
    sortedSubscriptions: Array,
    totalPrice: Number,
    sortBy: String
  },

  emits: [
    "update-sort",
    "edit-item",
    "delete-item"
  ]
};
</script>