<template>
    <el-table ref="tableRef" row-key="controlId" :data="controlData" style="width: 100%">
        <el-table-column
            prop="controlId"
            label="ControlId"
            sortable
            width="180"
            column-key="controlId"
            :filters="[
                { text: 'S3.2', value: 'S3.2' },
                { text: 'RDS.11', value: 'RDS.11' }
            ]"
            :filter-method="filterHandler"
        />
        <el-table-column prop="description" label="Description" width="180" />
    </el-table>
</template>