<template>
    <div style="padding: 20px;">
        <el-button style="margin-bottom: 20px;" type="primary" @click="getDetail">Refresh</el-button>
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
}

onMounted(() => {
    getDetail();
})
</script>

<style lang="scss" scoped></style>