<template>
  <el-table ref="tableRef" row-key="controlId" :data="filterTableData" style="width: 100%">
    <el-table-column prop="ControlId" label="ControlId" sortable width="180" column-key="ControlId" :filters="[
      { text: 'aws-foundational-security-best-practices', value: 'arn:aws:securityhub:ap-southeast-1::standards/aws-foundational-security-best-practices/v/1.0.0' },
      { text: 'cis-aws-foundations-benchmark', value: 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0' }
    ]" :filter-method="filterHandler" />
    <el-table-column prop="Title" label="Title" width="200" />
    <el-table-column prop="ControlStatus" :filters="[
      { text: 'ENABLED', value: 'ENABLED' },
      { text: 'DISABLED', value: 'DISABLED' }
    ]" label="ControlStatus" width="180" :filter-method="filterHandler" />
    <!-- <el-table-column prop="RelatedRequirements" label="RelatedRequirements" width="180" /> -->
    <el-table-column prop="SeverityRating" :filters="[
      { text: 'LOW', value: 'LOW' },
      { text: 'MEDIUM', value: 'MEDIUM' },
      { text: 'HIGH', value: 'HIGH' },
      { text: 'CRITICAL', value: 'CRITICAL' }
    ]" :filter-method="filterHandler" label="SeverityRating" width="180">
      <template #default="scope">
        <el-button link v-if="scope.row.SeverityRating == 'LOW'" type="info">{{ scope.row.SeverityRating.toLowerCase() }}</el-button>

        <el-button link v-if="scope.row.SeverityRating == 'MEDIUM'">{{ scope.row.SeverityRating.toLowerCase() }}</el-button>

        <el-button link v-if="scope.row.SeverityRating == 'HIGH'" type="warning">{{ scope.row.SeverityRating.toLowerCase() }}</el-button>

        <el-button link v-if="scope.row.SeverityRating == 'CRITICAL'" type="danger">{{ scope.row.SeverityRating.toLowerCase() }}</el-button>
      </template>
    </el-table-column>
    <el-table-column prop="ReactorId" label="ReactorId" width="180" />
    <el-table-column label="Operations">
      <template #header>
        <el-input v-model="search" size="small" placeholder="Type Control ID to search" />
      </template>
      <template #default="scope">
        <el-button link type="primary" size="small" @click="handleConfigure(scope.$index, scope.row)">
          Configure
        </el-button>
      </template>
    </el-table-column>
    <!-- <el-table-column prop="RemediationUrl" label="Reference" width="180" /> -->
  </el-table>
  <el-dialog v-model="dialogConfigureFormVisible" title="Configure">
    <el-form :model="updateControlPayload">
      <el-form-item label="Reactor" label-width="140px">
        <el-select v-model="updateControlPayload.ReactorId" placeholder="Please select a zone">
          <template v-for="item in options" :key="item.reactorId">
            <el-option v-if="item.controlId == selectedControl.ControlId" :label="item.reactorId"
              :value="item.reactorId" />
          </template>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogConfigureFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="updateControl">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { da } from 'element-plus/es/locale';
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'
import { env } from 'process';

const dialogConfigureFormVisible = ref(false);
const updateControlPayload = reactive({
  ReactorId: ''
})
const selectedControl = reactive(
  {
    ControlId: ""
  }
)
const reactorSelectorLoading = ref(false);
const url = "https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/controls";
const { data: resp, pending, refresh, error } = await useFetch(url);
console.log(resp.value)
let controlData: Control[] = reactive(resp.value.data);

const search = ref('')

const filterTableData = computed(() =>
  controlData.filter(
    (data) =>
      !search.value ||
      data.ControlId.toLowerCase().includes(search.value.toLowerCase())
  )
)

interface Control {
  RelatedRequirements: Array<string>;
  Title: string;
  RemediationUrl: string;
  ControlStatus: string;
  updatedAt: string;
  SeverityRating: string;
  ControlStatusUpdatedAt: string;
  ControlId: string;
  createdAt: string;
  StandardsControlArn: string;
  Description: string;
}

const filterHandler = (
  value: string,
  row: Control,
  column: TableColumnCtx<Control>
) => {
  let property = ""
  if (column['property'] == "ControlId") {
    property = "StandardsArn"
  }
  else {
    property = column['property']
  }
  console.log(property)
  return row[property] === value
}

const updateControl = async () => {
  console.log("updateControl called")
  const { data: resp } = await useFetch("https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/controls/" + selectedControl.ControlId, {
    method: "put",
    body: updateControlPayload
    // headers: {
    //   'x-api-key': updateControlPayload.value
    // }
  })
  console.log(resp)
  dialogConfigureFormVisible.value=false
}
const handleConfigure = (index, row) => {
  dialogConfigureFormVisible.value = true
  selectedControl.ControlId = row.ControlId
  console.log(row.ControlId)
}

const handleDelete = (index, row) => {
  console.log()
}

const states = [
  'Alabama',
  'Alaska',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'Florida',
  'Georgia',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Pennsylvania',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming',
]

interface ListItem {
  value: string
  label: string
}

const list = states.map((item): ListItem => {
  return { value: `value:${item}`, label: `label:${item}` }
})

interface Reactor {
  RelatedRequirements: Array<string>;
  repo: string;
  reactorId: string;
  updatedAt: string;
  createdAt: string;
  controlId: string;
  description: string;
  resource: Map<string, string>;
}


const { data: reactors } = await useFetch("https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/reactors");
console.log(reactors.value)
let options = reactive(reactors.value.data);

const handleFix = (index, row) => {
  console.log(index, row)
}
</script>
<style scoped>
.el-button--text {
  margin-right: 15px;
}

.el-select {
  width: 300px;
}

.el-input {
  width: 300px;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>
