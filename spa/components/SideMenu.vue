<template>
    <el-menu router :default-active="props.activeItem" class="el-menu-vertical-demo" @open="handleOpen"
        @close="handleClose">
        <el-sub-menu index="1">
            <template #title>
                <el-icon>
                    <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-029747aa="">
                        <path fill="currentColor"
                            d="M320 256a64 64 0 0 0-64 64v384a64 64 0 0 0 64 64h384a64 64 0 0 0 64-64V320a64 64 0 0 0-64-64H320zm0-64h384a128 128 0 0 1 128 128v384a128 128 0 0 1-128 128H320a128 128 0 0 1-128-128V320a128 128 0 0 1 128-128z">
                        </path>
                        <path fill="currentColor"
                            d="M512 64a32 32 0 0 1 32 32v128h-64V96a32 32 0 0 1 32-32zm160 0a32 32 0 0 1 32 32v128h-64V96a32 32 0 0 1 32-32zm-320 0a32 32 0 0 1 32 32v128h-64V96a32 32 0 0 1 32-32zm160 896a32 32 0 0 1-32-32V800h64v128a32 32 0 0 1-32 32zm160 0a32 32 0 0 1-32-32V800h64v128a32 32 0 0 1-32 32zm-320 0a32 32 0 0 1-32-32V800h64v128a32 32 0 0 1-32 32zM64 512a32 32 0 0 1 32-32h128v64H96a32 32 0 0 1-32-32zm0-160a32 32 0 0 1 32-32h128v64H96a32 32 0 0 1-32-32zm0 320a32 32 0 0 1 32-32h128v64H96a32 32 0 0 1-32-32zm896-160a32 32 0 0 1-32 32H800v-64h128a32 32 0 0 1 32 32zm0-160a32 32 0 0 1-32 32H800v-64h128a32 32 0 0 1 32 32zm0 320a32 32 0 0 1-32 32H800v-64h128a32 32 0 0 1 32 32z">
                        </path>
                    </svg>
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
    CPU,
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