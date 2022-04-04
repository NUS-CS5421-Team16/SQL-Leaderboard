<template>
    <div style="padding: 20px;">
        <div class="operation">
            <el-button class="search-btn" type="primary" @click="getPublicRankList">Refresh</el-button>
            <upload @uploadSuccess="handleClick"></upload>
        </div>

        <el-tabs v-model="tabChoose" class="demo-tabs" @tab-click="handleClick">
            <el-tab-pane label="Leaderboard-Public" name="first">
                <vxe-table
                    :data="publicTableData"
                    v-loading="loading"
                    empty-text="No data"
                    v-if="tabChoose === 'first'"
                >
                    <vxe-table-column field="index" title="#"></vxe-table-column>
                    <vxe-table-column field="team_name" title="Team Name"></vxe-table-column>
                    <vxe-table-column field="entries" title="Entries"></vxe-table-column>
                    <vxe-table-column title="Time">
                        <template #default="scope">
                            <span
                                v-if="scope.row.running_time && scope.row.running_time !== '-'"
                            >{{ scope.row.running_time }}ms</span>
                            <span
                                v-else-if="scope.row.running_time && scope.row.running_time === '-'"
                            >-</span>
                        </template>
                    </vxe-table-column>
                </vxe-table>
            </el-tab-pane>
            <el-tab-pane label="Leaderboard-Private" name="second">
            <!-- <el-tab-pane label="Leaderboard Private" name="second" v-if="isCompetiionEnd"> -->
            <vxe-table
                :data="privateTableData"
                v-loading="loading"
                empty-text="No data"
                v-if="tabChoose === 'second'"
            >
              <vxe-table-column field="index" title="#"></vxe-table-column>
              <vxe-table-column field="team_name" title="Team Name"></vxe-table-column>
              <vxe-table-column field="entries" title="Entries"></vxe-table-column>
              <vxe-table-column title="Time">
                <template #default="scope">
                            <span
                                v-if="scope.row.running_time && scope.row.running_time !== '-'"
                            >{{ scope.row.running_time }}ms</span>
                  <span
                      v-else-if="scope.row.running_time && scope.row.running_time === '-'"
                  >-</span>
                </template>
              </vxe-table-column>
            </vxe-table>
          </el-tab-pane>
            <el-tab-pane label="Current User Result" name="third">
                <vxe-table
                    :data="userTableData"
                    v-loading="loading"
                    empty-text="No data"
                    v-if="tabChoose === 'third'"
                >
                    <vxe-table-column field="index" title="#"></vxe-table-column>
                    <vxe-table-column field="team_name" title="Team"></vxe-table-column>
                    <vxe-table-column field="competitor_name" title="Competitor Name"></vxe-table-column>
                    <vxe-table-column field="status" title="Status"></vxe-table-column>
                    <vxe-table-column field="error_message" title="Error Msg">
                        <template #default="scope">
                            <span
                                v-if="scope.row.error_message"
                                class="msg-overhide"
                                @click="showMsg(scope.row.error_message)"
                            >{{ scope.row.error_message }}</span>
                        </template>
                    </vxe-table-column>
                    <vxe-table-column field="start_time" title="Upload Time"></vxe-table-column>
                    <vxe-table-column title="Running Time">
                        <template #default="scope">
                            <span v-if="scope.row.result">{{ scope.row.result }}ms</span>
                        </template>
                    </vxe-table-column>
                    <vxe-table-column label="Operations">
                        <template #default="scope">
                            <el-button
                                size="small"
                                @click="download(scope.$index, scope.row)"
                            >Download</el-button>
                        </template>
                    </vxe-table-column>
                </vxe-table>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { useStore } from "vuex";
import { getCompetitionRank, getCompetitor } from '@/api';
// import { getCompetitionRank, getCompetitor, getCompetitionApi } from '@/api';
import { ElMessage, ElMessageBox } from 'element-plus'
import upload from './components/upload.vue'
import { config } from "@/utils/config";
import axios from "axios";


const store = useStore();
const state = reactive({
    cid: computed(() => sessionStorage.getItem('cid')),
})

const publicTableData = ref([]);
const privateTableData = ref([]);
const userTableData = ref([]);
const loading = ref(false);
const tabChoose = ref('first');
// const isCompetiionEnd = ref(false);

const handleClick = () => {
    if (tabChoose.value === 'first') {
        getPublicRankList();
    } else if (tabChoose.value === 'second') {
        getPrivateRankList();
    } else if (tabChoose.value === 'third') {
        getCompetitorTask();
    }
}

const getPublicRankList = async () => {
    loading.value = true;
    const params = {
        private: 0,
    }
    // const competitionInfo: any = await getCompetitionInfo()
    // // competition end
    // if (competitionInfo.end_time && new Date(competitionInfo.end_time).getTime() <= new Date().getTime()) {
    //     isCompetiionEnd.value = true;
    //     params.private = 0
    // }

    const res = await getCompetitionRank(params);
    publicTableData.value = formatData(res) || [];
    // set loading
    setTimeout(() => {
        loading.value = false;
    }, 300);
}

const getPrivateRankList = async () => {
    loading.value = true;
    const params = {
      private: 1,
    }
    const res = await getCompetitionRank(params);
    privateTableData.value = formatData(res) || [];
    // set loading
    setTimeout(() => {
      loading.value = false;
    }, 300);
}

const getCompetitorTask = async () => {
    const res = await getCompetitor(sessionStorage.getItem('cid'));

    const tasks = (res as any).tasks || [];

    const len = tasks.length;
    // set order for tasks
    tasks.forEach((task: any, index: number) => {
        task.index = len - index;
    })

    userTableData.value = (res as any).tasks

    setTimeout(() => {
        loading.value = false;
    }, 300);
}

const formatData = (res: any): any => {
    let list: any = [];
    // format data
    const keys = Object.keys(res);
    if (keys.length > 0) {
        const sortKeys = keys.sort();

        let otherTeams: any = [];
        let lastIdx: number = 0;
        sortKeys.forEach(key => {
            if (key === '-1') {
                otherTeams.push(...res[key]);
                return;
            } else {
                const item = res[key];
                item.index = key;
                lastIdx = +key;
                list.push(item);
            }
        })

        otherTeams.forEach((item: any, index: number) => {
            item.index = ++lastIdx;
            if (!item.entries) {
                item.entries = '-'
            }
            if (!item.running_time) {
                item.running_time = '-'
            }
            list.push(item);
        })
    }
    return list
}

const download = (index: number, row: any) => {
    let requestUrl = config.host + `/competition/${state.cid}/task/?tid=${row.id}`
    axios.get(requestUrl, { responseType: 'blob' })
        .then((res) => {
            const { data, headers } = res
            const fileName = 'download.sql'
            const blob = new Blob([data], { type: headers['content-type'] })
            let dom = document.createElement('a')
            let url = window.URL.createObjectURL(blob)
            dom.href = url
            dom.download = decodeURI(fileName)
            dom.style.display = 'none'
            document.body.appendChild(dom)
            dom.click()
            dom.parentNode.removeChild(dom)
            window.URL.revokeObjectURL(url)
        }).catch((err) => { })
}

const showMsg = (msg: string) => {
    ElMessageBox.alert(msg, 'Error msg', {
        confirmButtonText: 'OK',
    })
}

// dom ready
onMounted(async () => {
    getPublicRankList();
})
</script>

<style lang="scss" scoped>
.operation {
    display: flex;
    margin-bottom: 20px;

    .search-btn {
        margin-right: 10px;
    }
}
.msg-overhide {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 100%;
    // width: 150px;
    display: inline-block;
}
</style>