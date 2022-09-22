<template>
    <el-table ref="tableRef" row-key="reactorId" :data="filterTableData" style="width: 100%">
        <el-table-column
            min-width="140"
            prop="reactorId"
            label="Reactor"
            sortable
            column-key="reactorId"
            :filters="[
                { text: 'S3.2', value: 'S3.2' },
                { text: 'RDS.11', value: 'RDS.11' }
            ]"
            :filter-method="filterHandler"
        />
        <el-table-column prop="controlId" label="ControlId" />
        <el-table-column prop="description" label="Description" />
        <el-table-column prop="repo" label="Repo" min-width="180">
                    <template #default="scope">
                <el-button 
                link
                type="primary" size="small"
                    @click="handleNav(scope.$index, scope.row)"> {{scope.row.repo}} </el-button>
            </template>
        </el-table-column>
        <!-- <el-table-column prop="RelatedRequirements" label="RelatedRequirements" width="180" /> -->
        <el-table-column label="Actions">
            <template #header>
                <el-input v-model="search" size="small" placeholder="Type Control ID to search" />
            </template>
            <template #default="scope">
                <!-- <el-button 
                size="small" 
                @click="handleConfigure(scope.$index, scope.row)"
                >Update</el-button
                > -->
                <el-button 
                size="small" 
                link
                type="primary"
                @click="handleInstall(scope.$index, scope.row)"
                >Install</el-button
                >
            </template>
        </el-table-column>
        <!-- <el-table-column prop="RemediationUrl" label="Reference" width="180" /> -->
    </el-table>
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { da } from 'element-plus/es/locale';
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'

const url = "https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/hub/reactors";
const { data: resp, pending, refresh, error } = await useFetch(url);
console.log(resp.value)
let reactorData: Reactor[] = reactive(resp.value.data);

const search = ref('')

const filterTableData = computed(() =>
    reactorData.filter(
        (data) =>
            !search.value ||
            data.controlId.toLowerCase().includes(search.value.toLowerCase())
    )
)

const dialogInstallFormVisible = ref(false);
const installReactorPayload = reactive({
  ReactorId: '',

})

interface Reactor {
  RelatedRequirements: Array<string>;
  repo: string;
  reactorId: string;
  updatedAt: string;
  createdAt: string;
  controlId: string;
  description: string;
  resource: Map<string,string>;
}

const filterHandler = (
data
) =>  {
  
    console.log(data);
}

const handleInstall = (index, row) => {
  console.log(index, row)

}
const handleDelete = (index, row) => {
  console.log(index, row)
}

const handleNav = (index, row) => {
  console.log(index, row)
}
</script>