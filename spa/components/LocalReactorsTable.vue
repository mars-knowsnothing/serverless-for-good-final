<template>
    <el-table ref="tableRef" row-key="reactorId" :data="filterTableData" style="width: 100%">
        <el-table-column min-width="140" prop="reactorId" label="Reactor" sortable column-key="reactorId" />
        <el-table-column prop="controlId" label="ControlId" />
        <el-table-column prop="description" label="Description" />
        <el-table-column prop="repo" label="Repo" min-width="180">
            <template #default="scope">
                <el-button link type="primary" size="small" @click="handleNav(scope.$index, scope.row)">
                    {{ scope.row.repo }} </el-button>
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
                <el-button v-if="scope.row.installationStatusColor" size="small" link
                    :type="scope.row.installationStatusColor" @click="handleUninstall(scope.$index, scope.row)">
                    {{ scope.row.installationStatus }}
                </el-button>
                <el-button v-else size="small" link type="danger" @click="handleUninstall(scope.$index, scope.row)">
                    Uninstall
                </el-button>


            </template>
        </el-table-column>
        <!-- <el-table-column prop="RemediationUrl" label="Reference" width="180" /> -->
    </el-table>
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ElNotification } from 'element-plus'

import { da } from 'element-plus/es/locale';
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'

const url = "https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/reactors";
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

const filterHandler = (
    data
) => {

    console.log(data);
}

const installationStatus = ref("Uninstall");
const installationStatusColor = ref("danger");


const handleUninstall = async (index, row) => {
    console.log(index, row)
    row.installationStatus = "Uninstalling"
    row.installationStatusColor = "warning"
    ElNotification({
        title: 'Reactor Installer',
        message: 'Uninstallation Started',
        type: 'info',
    })
    const { data: resp } = await useFetch(
        "https://g8bfit35p3.execute-api.ap-southeast-1.amazonaws.com/dev/resources/reactors/" + row.reactorId,
        {
            method: "delete"
        }
    )
    ElNotification({
        title: 'Reactor Installer',
        message: 'Uninstallation Completed',
        type: 'success',
    })
    row.installationStatus = "install"
    row.installationStatusColor = "primary"
    // setTimeout(() => {
    //     ElNotification({
    //         title: 'Reactor Installer',
    //         message: 'Uninstallation Completed',
    //         type: 'success',
    //     })
    //     row.installationStatus = "install"
    //     row.installationStatusColor = "primary"
    // }, 5000);
}
const handleUpdate = (index, row) => {
    console.log(index, row)
}

const handleNav = (index, row) => {
    console.log(index, row)
}
</script>