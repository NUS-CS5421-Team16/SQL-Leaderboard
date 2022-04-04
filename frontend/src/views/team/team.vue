<template>
    <div style="padding: 20px;">
        <el-container>
            <el-button style="margin-bottom: 20px;" type="primary" @click="getDetail">Refresh</el-button>
        </el-container>
        <el-row>
            <h1>
                Teammates Info
            </h1>
            <el-table
                :data="teammateTableData"
                stripe
                style="width: 100%">
                <el-table-column prop="competitor id" label="competitor id"></el-table-column>
                <el-table-column prop="name" label="name"></el-table-column>
            </el-table>
        </el-row>
        <el-row>
            <h1>Change Team Info</h1>
        </el-row>
        <el-row>
            <div>Two Usages:</div>
        </el-row>
        <el-row>
            <div>1. Change your Team: input your target Team Name and Team UUID, then click "update".</div>
        </el-row>
        <el-row>
            <div>2. Change your Team Name: only input new Team Name and leave UUID unchanged, then click "update".</div>
        </el-row>
        <el-form :model="form" label-width="120px">
            <el-form-item label="Team Name">
                <el-input v-model="form.team_name" />
            </el-form-item>
            <el-form-item label="Team UUID">
                <el-input v-model="form.team_uuid" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Update</el-button>
            </el-form-item>
        </el-form>

    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useStore } from "vuex";
import { getCompetitor, updateTeam } from '@/api'
import { ElMessage } from 'element-plus'

const store = useStore();
const state = reactive({
    cid: computed(() => sessionStorage.getItem('cid')),
})

const teammateTableData = ref([]);

const form = reactive({
    team_name: '',
    team_uuid: '',
})

const onSubmit = async () => {
    let submitted_data = new FormData();
    submitted_data.append('team_name',form.team_name)
    submitted_data.append('team_uuid',form.team_uuid)
    const res = await updateTeam(sessionStorage.getItem('cid'), submitted_data)
    if (res) {
        ElMessage.success('update Success')
    }
    getDetail()
}

const getDetail = async () => {
    const res = await getCompetitor(sessionStorage.getItem('cid'));
    form.team_name = (res as any).team_name;
    form.team_uuid = (res as any).team_uuid;
    teammateTableData.value = (res as any).teammates;
}

onMounted(() => {
    getDetail();
})
</script>

<style lang="scss" scoped>
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
</style>