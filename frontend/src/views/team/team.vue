<template>
    <div style="padding: 20px;">
        <el-button style="margin-bottom: 20px;" type="primary" @click="getDetail">Refresh</el-button>
        <el-form :model="form" label-width="120px">
            <el-form-item label="Team Name">
                <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="Team ID">
                <el-input v-model="form.id" />
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
    cid: computed(() => store.getters.getCid),
})

const form = reactive({
    name: '',
    id: '',
})

const onSubmit = async () => {
    const res = await updateTeam(state.cid, form)
    if (res) {
        ElMessage.success('update Success')
    }
    getDetail()
}

const getDetail = async () => {
    const res = await getCompetitor(state.cid);
    form.name = (res as any).name;
    form.id = (res as any).id;
}

onMounted(() => {
    // store.commit("setCid", '12212121');
    getDetail();
})
</script>

<style lang="scss" scoped></style>