<template>
    <el-table v-loading="loading" ref="tableRef" row-key="Id" :data="filterTableData" style="width: 100%">
        <el-table-column prop="Id" label="Finding Id" sortable column-key="reactorId" :filters="[
            { text: 'aws-foundational-security-best-practices', value: 'arn:aws:securityhub:ap-southeast-1::standards/aws-foundational-security-best-practices/v/1.0.0' },
            { text: 'cis-aws-foundations-benchmark', value: 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0' }
        ]" :filter-method="filterHandler" />
        <el-table-column prop="Title" label="Title" />
        <el-table-column prop="AwsAccountId" label="Account" />
        <el-table-column prop="Resources" label="Resources">
            <template #default="scope">
                <template v-for="res in scope.row.Resources">
                    {{res.Type}} - {{res.Id}}
                </template>
            </template>
        </el-table-column>
        <el-table-column prop="Reactor" label="Reactor">
            <template #default="scope">
                <el-button v-if="scope.row.Reactor == 'not configured'" type="danger" link size="small">
                    {{ scope.row.Reactor }} </el-button>
                <el-button v-else link type="success" size="small"> {{ scope.row.Reactor }} </el-button>
            </template>
        </el-table-column>
        <el-table-column>
            <template #header>
                <el-input v-model="search" size="small" placeholder="Type Control ID to search" />
            </template>
            <template #default="scope">
                <el-button link :disabled="processing" type="primary" v-if="scope.row.Reactor != 'not configured'"
                    size="small" @click="handleRemediation(scope.$index, scope.row)"> {{ scope.row.remediationStatus ?
                            scope.row.remediationStatus : "Remediate"
                    }} </el-button>
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
import { ElNotification } from 'element-plus'
import { Row } from 'element-plus/es/components/table-v2/src/components';

const loading = ref(true)

let findingData: Finding[] = reactive([]);

const createExecutionPayload = reactive({
    stateMachineInput: {},
    options: {}
})
const pageLoading = true
const url = "https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/findings";
const { data: resp, pending, refresh, error } = await useFetch(url);
console.log(resp.value)
findingData = resp.value.data

loading.value = false;

interface Finding {
    Id: string;
    GeneratorId: string;
    AwsAccountId: string;
    Types: string;
    Title: string;
}

const processing = ref(false)
const filterHandler = (
    value: string,
    row: Finding,
    column: TableColumnCtx<Finding>
) => {
    const property = column['property']
    return row[property] === value
}

const handleRemediation = async (index, row) => {
    console.log(index, row)
    createExecutionPayload.stateMachineInput = { detail: { findings: [row] } }
    ElNotification({
        title: 'Fix Security Hub Finding',
        message: 'Remediation Started',
        type: 'success',
    })
    processing.value = true
    row.remediationStatus = "Processing"
    // setTimeout(() => {
    //     ElNotification({
    //         title: 'Fix Security Hub Finding',
    //         message: 'Reactor Execution Completed',
    //         type: 'success',
    //     })
    // }, 15000);
    const { data: resp } = await useFetch("https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/services/state-machine/SecurityHubFindingReactor/executions", {
        method: "post",
        body: createExecutionPayload
        // headers: {
        //   'x-api-key': updateControlPayload.value
        // }
    })
    console.log(resp.value)
    ElNotification({
        title: 'Fix Security Hub Finding',
        message: 'Reactor Execution Completed',
        type: 'success',
    })
    setTimeout(() => {
        ElNotification({
            title: 'Fix Security Hub Finding',
            message: 'Notification Sent To Wechat',
            type: 'success',
        })
    }, 20000);

    setTimeout(() => {
        ElNotification({
            title: 'Fix Security Hub Finding',
            message: 'Remediation Completed',
            type: 'success',
        })
        row.remediationStatus = "Remediate"
        processing.value = false
    }, 25000);

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