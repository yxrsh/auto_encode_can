#!/usr/bin




cb_fullmatch_temp='''
	$DATA_TYPE	$DATA_NAME;  // [${MIN_VAL}, ${MAX_VAL}] ${INVALID} ${FACTOR}${OFFSET}${UNIT}${MEANING}${DESCRIPTION}'''

cb_fullmatch_reserved='''
	$DATA_TYPE	reserved_B${START_BYTE}${END_BYTE};'''

cb_partmatch_reserved='''
			$DATA_TYPE	reserved_b${START_BIT}${END_BIT}		: $DATA_LENGTH;'''

cb_partmatch_reserved_none='''
			$DATA_TYPE				: $DATA_LENGTH;'''

cb_partmatch_temp='''
			$DATA_TYPE	$DATA_NAME		: $DATA_LENGTH;	// [${MIN_VAL},${MAX_VAL}] ${INVALID} ${FACTOR}${OFFSET}${UNIT}${MEANING}${DESCRIPTION}'''

cb_partmatch_head='''
	union{
		struct{$DATA_BODY
		} bits;
		$FMT_TYPE vals;
	} B${START_BYTE}${END_BYTE};'''

cb_frame_tmp = '''
// id:${CANID} $PERIOD $COMMENT
struct can${RDWR}_${NAME} {$FRAME_BODY	
}__attribute__((packed));
'''



fl_head_string = '''// Copyright (C) 2019 - Minieye INC.

#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>

#include <sys/timerfd.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>

#include <errno.h>
#include <linux/can/error.h>

#include "gflags/gflags.h"
#include "unified_process_rsp.h"


#define CAN_DEVICE				"${CAN_CHANNEL}"	// 根据实际产品定义CAN通道
#define PERIOD_SLEEP_MS			${PERIOD_TIME}		// 每次循环睡眠50ms
#define ENABLE_SEPARATE_SEND	0		// 是否独立一个线程发送CAN报文
$MACRO_CANSEND

#define min(x, y)			((x) > (y) ? (y) : (x))		// 取较小值
#define max(x, y)			((x) > (y) ? (x) : (y))		// 取较大值
#define mid(val, x, y)		(max(min((val), (y)), (x)))	// 取中间值


// declare gflag below
DECLARE_double(ldw_speed_thresh);


'''

can_send_msg_temp='''
	{.id = $ID, .type = PERIOD, .delay = $DELAY,  .msg = (uint8_t*)&$MSG, .len = $LEN},'''

can_send_temp='''

/***************************** CAN发送数据相关变量 **************************/
enum CAN_PACKET_TYPE{EVENT = 0, PERIOD, EVENT_PERIOD};
struct can_transmint_type_t{
	uint32_t id;		// CAN id
	uint8_t type;		// 0=事件型, 1=周期型, 2=事件周期型
	uint32_t delay;		// 事件型or周期型每帧之间的延时
	uint8_t *msg;		// CAN数据缓存
	uint8_t len;		// 缓存区大小
	uint32_t delay_ev;	// 事件周期型中，事件触发后的延时
	uint8_t event_nums;	// 事件周期型中，事件触发后，以事件型延时发送的报文次数
};

// CAN 发送数据相关信息
struct can_transmint_type_t can_transmit_id_list[NUM_OF_SEND_ID]={
	/* 如果为周期型，只需要填充 */
	/* id   帧类型  周期延时  事件延时   事件CAN帧数   发送BUFF */$FRAME_LIST
};
'''


func_lds_temp = '''
void do_lane_detect_rsp(struct LaneDetectRsp_all *lds) {
    static long long int time_base = 0;
    struct timeval tv;
    gettimeofday(&tv, NULL);
    LOG_LDS("%lld|frame_id:%u\\n",
            (tv.tv_sec*1000 + tv.tv_usec/1000) - time_base,
                lds->rsp.frame_id);
    time_base = tv.tv_sec*1000 + tv.tv_usec/1000;
	
	char timestr[30];
	struct tm tm = *localtime(&tv.tv_sec);
	strftime(timestr, 29, "%Y-%m-%d %H:%M:%S", &tm);
	LOG_LDS("(%s.%lu):\\n", timestr, tv.tv_usec);

	if (lds == NULL)
		return;
	
	// TODO

	for (size_t i = 0; i < lds->rsp.lanelines.size(); i++)
	{
		// TODO
	}

	// TODO

}
'''

func_vds_temp = '''
void do_vehicle_detect_rsp(struct VehicleDetectRsp_all *vds) {
	static long long int time_base = 0;
	struct timeval tv;
	gettimeofday(&tv, NULL);
	LOG_VDS("%lld|frame_id:%u\\n",
	        (tv.tv_sec*1000 + tv.tv_usec/1000) - time_base,
	            vds->frame_id);
	time_base = tv.tv_sec*1000 + tv.tv_usec/1000;

	if (vds == NULL)
	{
		LOG_VDS("input ptr invalid\\n");
		return;
	}
	
	// TODO
	
	for (size_t idx = 0; idx < vds->rsp.dets.size(); idx++)
	{
		// TODO
	}

	// TODO
	
}
'''

func_pds_temp = '''
void do_people_detect_rsp(struct PeopleDetectRsp_all *pds) {
	static long long int time_base = 0;
	struct timeval tv;
	gettimeofday(&tv, NULL);
	LOG_PDS("%lld|frame_id:%lld\\n",
		    (tv.tv_sec*1000 + tv.tv_usec/1000) - time_base,
		        rsp->processed_frame_id);
	time_base = tv.tv_sec*1000 + tv.tv_usec/1000;

	struct tm tm = *localtime(&tv.tv_sec);
	char timestr[30];		
	strftime(timestr, 29, "%Y-%m-%d %H:%M:%S", &tm);
	LOG_PDS("(%s.%03ld)\\n", timestr, tv.tv_usec/1000); 

	if (pds == NULL)
	{
		LOG_PDS("input ptr invalid\\n");
		return;
	}

	// TODO

	for (size_t idx = 0; idx < pds->rsp.pedestrians.size(); idx++)
	{
		// TODO

	}
	
	// TODO

}
'''


func_tds_temp = '''
void do_tsr_detect_rsp(struct TsrDetectRsp_all *tds) {
	static long long int time_base = 0;
	struct timeval tv;
	gettimeofday(&tv, NULL);

	LOG_TDS("%lld|frame_id:%lld\\n",
			(tv.tv_sec*1000 + tv.tv_usec/1000) - time_base, frame_id);
	time_base = tv.tv_sec*1000 + tv.tv_usec/1000;

	struct tm tm = *localtime(&tv.tv_sec);
	char timestr[30];		
	strftime(timestr, 29, "%Y-%m-%d %H:%M:%S", &tm);
	LOG_TDS("(%s.%03ld)\\n", timestr, tv.tv_usec / 1000);

	if (tds == NULL)
	{
		LOG_TDS("input ptr invalid\\n");
		return;
	}

	// TODO

	for (size_t idx = 0; idx < tds->rsp.tsr_dets.size(); idx++)
	{
		// TODO
	}

	// TODO

}
'''

func_timer_temp = '''
int tmfd_sleep = -1;

static void timerfd_handler(int fd) {
    struct timeval tv1, tv2;
    uint64_t exp = 0;
    int ret = read(fd, &exp, sizeof(uint64_t));
    return;
}
static void sleep_period_ms(int tmfd) { timerfd_handler(tmfd); }

static int timerfd_init(int delay) {
    int tmfd;
    int ret;
    struct itimerspec new_value;
	
	if (delay <= 0)
	{
		return -1;
	}

    tmfd = timerfd_create(CLOCK_REALTIME, 0);
    if (tmfd < 0) {
        return -1;
    }

    struct timespec now;
    if (clock_gettime(CLOCK_REALTIME, &now) == -1) {
        assert(0);
    }

    new_value.it_value.tv_sec = now.tv_sec + 1;
    new_value.it_value.tv_nsec = now.tv_nsec;
    new_value.it_interval.tv_sec = 0;
    new_value.it_interval.tv_nsec = delay * 1000 * 1000;

    ret = timerfd_settime(tmfd, TFD_TIMER_ABSTIME, &new_value, NULL);
    if (ret < 0) {
        close(tmfd);
        return -1;
    }

    return tmfd;
}
'''

func_can_interface_temp = '''
/************************************** CAN发送接口配置及处理 **************************************/

static void can_transmit(uint32_t id, uint8_t *data, uint8_t len)
{
  	if (data == NULL || len > 8){
    	LOG_UPR("%s, intput error pData=%lld, len=%d\\n", __func__, (uint64_t)data, len);
		return;
	}

	struct can_frame fr;
	fr.can_id = id;
	if (fr.can_id > 0x7ff)
	{
		fr.can_id |= CAN_EFF_FLAG;
	}
	
	fr.can_dlc = len;
	memcpy(fr.data, data, fr.can_dlc);

  	if (sizeof(struct can_frame) != write(fd_can_send, &fr, sizeof(struct can_frame))){
    	LOG_UPR("can send fail\\n");
  	} else{
    	LOG_UPR("%x [%d] %02X %02X %02X %02X %02X %02X %02X %02X\\n", fr.can_id, fr.can_dlc,
       		fr.data[0], fr.data[1], fr.data[2], fr.data[3], fr.data[4], fr.data[5], fr.data[6], fr.data[7]);
  	}
}

'''

func_time_init_temp='''
/*************************** 定时器 ***************************/
int tmfd_50ms = -1;

void timerfd_handler(int fd) {
    struct timeval tv1, tv2;
    uint64_t exp = 0;
    int ret = read(fd, &exp, sizeof(uint64_t));
    return;
}
void sleep_period_ms(int tmfd) { timerfd_handler(tmfd); }

int timerfd_init(int delay) {
    int tmfd;
    int ret;
    struct itimerspec new_value;
	
	if (delay <= 0)
	{
		return -1;
	}

    tmfd = timerfd_create(CLOCK_REALTIME, 0);
    if (tmfd < 0) {
        return -1;
    }

    struct timespec now;
    if (clock_gettime(CLOCK_REALTIME, &now) == -1) {
        assert(0);
    }

    new_value.it_value.tv_sec = now.tv_sec + 1;
    new_value.it_value.tv_nsec = now.tv_nsec;
    new_value.it_interval.tv_sec = 0;
    new_value.it_interval.tv_nsec = delay * 1000 * 1000;

    ret = timerfd_settime(tmfd, TFD_TIMER_ABSTIME, &new_value, NULL);
    if (ret < 0) {
        close(tmfd);
        return -1;
    }

    return tmfd;
}
'''

func_dev_init_loopback_temp = '''
	// 本地回环功能是默认开启的，此处关闭CAN发送回环功能
	int loopback = 0;	
	if (0 > setsockopt(can_fd, SOL_CAN_RAW, CAN_RAW_LOOPBACK, &loopback, sizeof(loopback)))
	{
		LOG_UPR("setsockopt, disable loopback function failed\\n");
		close(can_fd);
		return -1;
	}
'''

func_dev_init_enablereceive_temp='''
	// 创建CAN接收线程
	pthread_t pth_can_rcv;
	int err = pthread_create(&pth_can_rcv, NULL, can_rcv_thread, NULL);
	if (err != 0)
	{
		LOG_UPR("pthread_create can_rcv_thread failed, error = %d\\n", err);
		return -1;
	}
'''


func_dev_init_disablereceive_temp='''
	// 屏蔽CAN接收功能，不接收任何CAN报文
	if (0 > setsockopt(can_fd, SOL_CAN_RAW, CAN_RAW_FILTER, NULL, 0)) {
		LOG_UPR("setsockopt");
		close(can_fd);
		return -1;
	}
'''

func_dev_init_send_split_temp='''
	// 创建CAN发送线程
	pthread_t pth_can_send;
	if (0 > pthread_create(&pth_can_send, NULL, can_send_thread, NULL)){
		close(can_fd);
		LOG_UPR("create can_rcv_thread failed\\n");
		return -1;
	}
'''

func_dev_init_temp = '''

/* 初始化CAN设备 */
int can_fd = -1;

static int can_dev_init(const char *dev)
{
	struct ifreq ifr;
	struct sockaddr_can addr;

	can_fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);
	if (can_fd < 0){
		LOG_UPR("socket failed\\n");
		return -1;
	}

	strcpy(ifr.ifr_name, dev);
	if (0 > ioctl(can_fd, SIOCGIFINDEX, &ifr)){
		LOG_UPR("ioctl, err=%s\\n", strerror(errno));
 		return -1;
	}

	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;
	if (0 > bind(can_fd, (struct sockaddr *)&addr, sizeof(addr))){
		LOG_UPR("bind failed\\n");
		close(can_fd);
		return -1;
	}

	// 初始化CAN发送定时器（精确延时）
	tmfd_50ms = timerfd_init(PERIOD_SLEEP_MS);
	if (tmfd_50ms < 0)
	{
		LOG_UPR("init timefd faile\\n");
		close(can_fd);
		return -1;
	}
${CAN_LOOPBACK}${CAN_RCV_INIT}${CAN_SEND_SPLIT}
	return 0;
}


'''

func_can_rcv_temp='''
void *can_rcv_thread(void *arg)
{
	struct can_frame fr;

	pthread_detach(pthread_self());
	pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL);
	while (1)
	{
		if (0 < read(can_fd, &fr, sizeof(fr)))
		{
			// TODO
		}
	}
}
'''
