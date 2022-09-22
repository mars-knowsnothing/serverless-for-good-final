<template>
    <el-table ref="tableRef" row-key="Id" :data="filterTableData" style="width: 100%">
        <el-table-column prop="Id" label="Finding Id" sortable column-key="reactorId" :filters="[
            { text: 'aws-foundational-security-best-practices', value: 'arn:aws:securityhub:ap-southeast-1::standards/aws-foundational-security-best-practices/v/1.0.0' },
            { text: 'cis-aws-foundations-benchmark', value: 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0' }
        ]" :filter-method="filterHandler" />
        <el-table-column prop="Title" label="Title" />
        <el-table-column prop="AwsAccountId" label="Account" />
        <el-table-column prop="Reactor" label="Reactor" >
            <template #default="scope">
                <el-button 
                v-if="scope.row.Reactor == 'not configured'" 
                type="danger" 
                link
                size="small"> {{scope.row.Reactor}} </el-button>
                <el-button 
                v-else 
                link
                type="success" size="small"> {{scope.row.Reactor}} </el-button>
            </template>
        </el-table-column>
        <el-table-column>
            <template #header>
                <el-input v-model="search" size="small" placeholder="Type Control ID to search" />
            </template>
            <template #default="scope">
                <el-button 
                link
                type="primary"
                v-if="scope.row.Reactor != 'not configured'" size="small"
                    @click="handleFix(scope.$index, scope.row)"> Remediate </el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { da } from 'element-plus/es/locale';
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'
import { env } from 'process';

const url = "https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/findings";
const { data: resp, pending, refresh, error } = await useFetch(url);
console.log(resp.value)
let findingData: Finding[] = reactive(resp.value.data);

interface Finding {
    Id: string;
    GeneratorId: string;
    AwsAccountId: string;
    Types: string;
    Title: string;
}

const filterHandler = (
    value: string,
    row: Finding,
    column: TableColumnCtx<Finding>
) => {
    const property = column['property']
    return row[property] === value
}

const handleFix = (index, row) => {
    console.log("handleFix called")
}
const search = ref('')

const filterTableData = computed(() =>
    findingData.filter(
        (data) =>
            !search.value ||
            data.Title.toLowerCase().includes(search.value.toLowerCase())
    )
)
</script>