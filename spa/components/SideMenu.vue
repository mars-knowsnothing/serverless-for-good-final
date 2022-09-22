<template>
    <el-menu 
    router
    :default-active="props.activeItem" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
        <el-sub-menu index="1">
            <template #title>
                <el-icon>
                    <location />
                </el-icon>
                <span>Control Panel</span>
            </template>
            <el-menu-item-group title="Security Hub">
                <el-menu-item index="/security-hub/controls" active>Control</el-menu-item>
                <el-menu-item index="/security-hub/findings">Finding</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="OPA">
                <el-menu-item index="/opa/policies" disabled>Policy</el-menu-item>
                <el-menu-item index="/opa/findings" disabled>Finding</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
        <el-sub-menu index="2">
            <template #title>
                <el-icon>
                    <icon-menu />
                </el-icon>
                <span> Repository</span>
            </template>
            <el-menu-item-group title="Official">
                <el-menu-item index="/repo/hub">Hub</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Community">
                <el-menu-item index="/repo/community" disabled>Community</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Local">
                <el-menu-item index="/repo/local">Local</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
    </el-menu>
</template>
<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const props = defineProps({
  activeItem: { type: String, required: true }
})

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>