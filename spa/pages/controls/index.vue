<template>
    <div class="common-layout">
        <el-container>
            <el-header><h1>Reactors</h1></el-header>
            <el-container>
                <el-aside width="200px">
                    <SideMenu/>
                </el-aside>
                <el-main>
                    <ReactorsTable />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>