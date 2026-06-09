<template>
    <div class="summary">
      <p>訂閱數量：{{ subscriptions.length }}</p>
      <p>每月總金額：約 NT$ {{ totalPrice }}</p>
</div>
<div class="chart-box">
      <h2>類別花費比例</h2>
      <Pie :data="categoryChartData" :options="chartOptions" />
</div>
<div class="table-header">

  <h2>訂閱清單</h2>

  <div class="form-row">
    <label>排序方式</label>
    <select
      :value="sortBy"
      @change="$emit('update-sort', $event.target.value)"
    >
      <option value="newest">由新到舊排序</option>
      <option value="oldest">由舊到新排序</option>
      <option value="category">依類別排序</option>
      <option value="payment">依扣款日排序</option>
    </select>
  </div>

</div>
    <table>
      <thead>
        <tr>
          <th>服務</th>
          <th>方案</th>
          <th>類別</th>
          <th>價格</th>
          <th>週期</th>
          <th>下次扣款日</th>
          
          
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
            "#A8B5A2", 
            "#C8B6A6", 
            "#B7A9C6", 
            "#9FB6C1", 
            "#D3C4B5", 
            "#C6A5A0" 
          ],
          borderColor: "#FFFFFF",
          borderWidth: 3
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
<style scoped>
.summary {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.summary p {
  flex: 1;
  padding: 20px;
  margin: 0;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  color: #222;
  font-size: 15px;
}

.chart-box {
  width: 100%;
  box-sizing: border-box;
  margin: 0 0 32px;
  padding: 28px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;

  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-box canvas {
  margin: 0 auto !important;
}
.chart-box h2 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 20px;
  font-weight: 500;
  color: #222;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.table-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 500;
  color: #222;
}

.sort-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sort-row label {
  font-size: 14px;
  color: #444;
}

select {
  padding: 9px 12px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  background: #fff;
  color: #000;
  font-size: 14px;
  outline: none;
}

select:focus {
  border-color: #888;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  overflow: hidden;
}

th {
  padding: 14px 12px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  background: #f7f7f7;
  border-bottom: 1px solid #e5e5e5;
}

td {
  padding: 14px 12px;
  font-size: 14px;
  color: #222;
  border-bottom: 1px solid #eeeeee;
}

tr:last-child td {
  border-bottom: none;
}

button {
  padding: 8px 12px;
  margin-right: 8px;
  border: 1px solid #222;
  border-radius: 8px;
  background: #222;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.delete {
  background: #fff;
  color: #222;
}

button:hover {
  opacity: 0.85;
}

</style>