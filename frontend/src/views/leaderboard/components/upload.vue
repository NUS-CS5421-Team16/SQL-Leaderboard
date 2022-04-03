<template>
    <el-upload
        ref="uploadRef"
        class="upload-demo"
        name="sql"
        :action="actionUrl"
        :auto-upload="false"
        :before-upload="beforeUpload"
        :on-success="handleSuccess"
        :on-error="handleError"
        :on-change="handleChange"
    >
        <template #trigger>
            <el-button class="choose" type="primary">Choose File</el-button>
        </template>

        <el-button class="submit" type="success" @click="submitUpload">Upload</el-button>
    </el-upload>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmit, reactive, computed } from 'vue';
import { useStore } from "vuex";
import { ElMessageBox } from 'element-plus'
import { config } from '@/utils/config'

const emit = defineEmit(['uploadSuccess'])

const uploadRef = ref()

const store = useStore();
const state = reactive({
    cid: computed(() => store.getters.getCid),
})

const actionUrl = ref(`${config.host}/competitor/${state.cid}/task/`);

const submitUpload = async () => {
    uploadRef.value!.submit()
}

const handleSuccess = (res: any) => {
    emit('uploadSuccess', res);
    uploadRef.value.clearFiles()
}

const handleError = (err: any) => {
    uploadRef.value.clearFiles()
    alertMsg();
}

const handleChange = (file: any, files: any) => {
    if (files.length > 1) {
        uploadRef.value.handleRemove(files[0])
    }
}

const beforeUpload = (file: any) => {
    const name = file.name
    if (!name.includes('.sql')) {
        ElMessageBox.alert('Please upload the sql file')
        return false
    } else {
        return;
    }
}

// message alert
const alertMsg = () => {
    ElMessageBox.alert('Please note that the file must not contain dangerous operations!', 'alert');
}
</script>

<style lang="scss" scoped>
.upload-demo {
    display: flex;
    position: absolute;
    left: 116px;
    .el-upload-list__item:first-child {
        transition: none;
    }
    .el-button--success {
        transition: none;
        height: 40px;
    }
    .choose {
        margin-right: 10px;
    }
}
</style>