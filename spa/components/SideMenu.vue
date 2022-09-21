<template>
    <el-menu default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
        <el-sub-menu index="1">
            <template #title>
                <el-icon>
                    <location />
                </el-icon>
                <span>Control Panel</span>
            </template>
            <el-menu-item-group title="Security Hub">
                <el-menu-item index="1-1">Control</el-menu-item>
                <el-menu-item index="1-2">Finding</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="OPA">
                <el-menu-item index="1-3">Policy</el-menu-item>
                <el-menu-item index="1-3">Finding</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item index="2">
            <el-icon>
                <icon-menu />
            </el-icon>
            <span>Repository</span>
        </el-menu-item>
    </el-menu>
</template>
<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>