<template>
    <div class="summary">
      <p>訂閱數量：{{ subscriptions.length }}</p>
      <p>每月總金額：約 NT$ {{ totalPrice }}</p>
</div>
<div class="chart-box">
      <h2>類別花費比例</h2>
      <Pie :data="categoryChartData" :options="chartOptions" />
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
          <th>下次扣款日</th>
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
          <td>{{ item.payment_day ? new Date(item.payment_day).toISOString().split("T")[0] : "" }}</td>
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
import { Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
  components: {
    Pie
  },

  props: {
    subscriptions: Array,
    sortedSubscriptions: Array,
    totalPrice: Number,
    sortBy: String
  },

  emits: ["update-sort", "edit-item", "delete-item"],

  computed: {
    categoryChartData() {
      const categoryMap = {};

      this.subscriptions.forEach((item) => {
        const category = item.category_name || "其他";
        const price = Number(item.price || 0);
        const cycle = Number(item.billing_cycle || 1);
        const monthlyPrice = price * (30 / cycle);

        if (!categoryMap[category]) {
          categoryMap[category] = 0;
        }

        categoryMap[category] += monthlyPrice;
      });

      return {
        labels: Object.keys(categoryMap),
        datasets: [
          {
            data: Object.values(categoryMap),
            backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40"
          ],
          borderWidth: 1
          }
        ]
      };
    },

    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom"
          }
        }
      };
    }
  }
};

</script>