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
import { ref, reactive, onMounted } from 'vue';
import { getCompetitor, updateTeam } from '@/api'
import { ElMessage } from 'element-plus'

const cid = ref('12312312')
const form = reactive({
    name: '',
    id: '',
})

const onSubmit = async () => {
    const res = await updateTeam(cid.value, form)
    if (res) {
        ElMessage.success('update Success')
    }
    getDetail()
}

const getDetail = async () => {
    const res = await getCompetitor(cid.value);
    form.name = (res as any).name;
    form.id = (res as any).id;
}

onMounted(() => {
    getDetail();
})
</script>

<style lang="scss" scoped></style>