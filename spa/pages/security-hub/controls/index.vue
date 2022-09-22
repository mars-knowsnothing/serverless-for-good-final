<template>
    <div class="common-layout">
        <el-container>
            <el-header><h1>Ouroboros - Security Reactor Framework</h1></el-header>
            <el-container>
                <el-aside width="200px">
                    <SideMenu active-item="/security-hub/controls"/>
                </el-aside>
                <el-main>
                    <ControlsTable />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>