#ifndef __UART_DEF__
#define __UART_DEF__

#define UART_MCU_TO_CAM            0x01   //cam is slave, uart data from MCU to cam.
#define UART_ACK_FROM_CAM2MCU      0x81   //ack from cam.

#define UART_PERI_TO_CAM           0x02   //cam is slave, uart data from peripheral to cam.
#define UART_ACK_FROM_CAM2PERI     0x82   //ack from cam.

#define UART_CAM_TO_PERI           0x04   //cam is host, uart data from cam to peripheral.
#define UART_ACK_FROM_PERI         0x84   //ack from peripheral.

enum {
    UART_NO_ERROR = 0x0,
    UART_ERROR_HOST_NOT_READY = 0x01,
    UART_ERROR_UART_CMD_NOT_SUPPORT,
    UART_ERROR_GENERIC = 0xff,
};

enum {
    RC_CODE_F1,
    RC_CODE_RETURN,
    RC_CODE_UP,
    RC_CODE_DOWN,
    RC_CODE_ESC,
    RC_CODE_F1_RELEASE,
    RC_CODE_RETURN_RELEASE,
    RC_CODE_UP_RELEASE,
    RC_CODE_DOWN_RELEASE,
    RC_CODE_ESC_RELEASE,

    RC_CODE_A_PRESSED = 0x64,
    RC_CODE_A_RELEASED,
    RC_CODE_B_PRESSED,
    RC_CODE_B_RELEASED,
    RC_CODE_C_PRESSED,
    RC_CODE_C_RELEASED,
    RC_CODE_D_PRESSED,
    RC_CODE_D_RELEASED,
    RC_CODE_A_FN_PRESSED,
    RC_CODE_A_FN_RELEASED,
    RC_CODE_B_FN_PRESSED,
    RC_CODE_B_FN_RELEASED,
    RC_CODE_C_FN_PRESSED,
    RC_CODE_C_FN_RELEASED,
    RC_CODE_D_FN_PRESSED,
    RC_CODE_D_FN_RELEASED,
};

// uart remote to camera
enum {
    UART_CMD_NONE = 0x0,
    UART_EMULATE_KEY,        // | cmd | RC_CODE_* |
                            // | ack | ok/ng |
    UART_SWITCH_TO_REC,      // | cmd |
                            // | ack | ok/ng |

    UART_SWITCH_TO_STILL,      // | cmd |
                            // | ack | ok/ng |

    UART_SWITCH_TO_PB,       // | cmd |
                            // | ack | ok/ng |
    UART_START_REC,          //5 | cmd |
                            // | ack | ok/ng |
    UART_STOP_REC,           // | cmd |
                            // | ack | ok/ng |
    UART_CAPTURE,            // | cmd |
                            // | ack | ok/ng |
    UART_CAPTURE_AF,         // | cmd |
                            // | ack | ok/ng |
    UART_AF,                 // | cmd |
                            // | ack | ok/ng |
    UART_START_PB,           //10 | cmd | folder index | file index[1] | file index[0]
                            // | ack | ok/ng |
    UART_STOP_PB,            // | cmd |
                            // | ack | ok/ng |
    UART_PAUSE_PB,           // | cmd |
                            // | ack | ok/ng |
    UART_RESUME_PB,          // | cmd |
                            // | ack | ok/ng |
    UART_SET_CONFIG,         // | cmd | key | type | value[n]
                            // | ack | ok/ng |
    UART_GET_CONFIG,         //15 | cmd | key |
    UART_SET_WIFI,           // | cmd | type |
                            // | ack | ok/ng |
    UART_GET_WIFI,           // | cmd |
                            // | ack | ok/ng | on/off |
    UART_GET_BATTERY,        // | cmd |
                            // | ack | ok/ng | battery |
    UART_GET_CARD_STATUS,    // | cmd |
                            // | ack | 0/1 |
    UART_GET_MODE,           //20 | cmd |
                            // | ack | ok/ng | mode|
    UART_GET_STATUS,         // | cmd |
                            // | ack | ok/ng | status |
    UART_GET_REC_REMAINING,  // | cmd |
                            // | ack | ok/ng | 4 byte(minutes)|
    UART_GET_STILL_REMAINING,// | cmd |
                            // | ack | ok/ng | 4 byte (amount of capture) |
    UART_FORMAT_CARD,        // | cmd |
                            // | ack |
    UART_GET_BT_VERSION,     //25 | cmd |
                            // | ack | ok/ng | major | minor |

    /* note: this cmd will disable camera timelapse or burst */
    UART_SWITCH_TO_MULTIPLE_MODE_CAPTURE,
    UART_SET_X_CONFIG,
    UART_GET_X_CONFIG,
    UART_QUERY_IS_RECORDING,
    UART_BURST_CAPTURE_START,
    UART_BURST_CAPTURE_CANCLE,
    UART_CLEAR_SETTING,     //32
    UART_INIT_PBMEDIA_FILE,
    UART_PBMEDIA_NEXT_FILE,
    UART_PBMEDIA_PREV_FILE,     //35
    UART_PBMEDIA_DELETE_FILE,
    UART_SHUT_DOWN,
    UART_LANC_CONTROL,
    UART_CRC_VALID_CONFIG,
    UART_PTZ_CONTROL,       //40
    UART_ASYN_MSG_EVENT,
    UART_ASYN_MSG_ENABLE,
    UART_CONFIG_UP_VALUE,
    UART_CONFIG_DOWN_VALUE,
    UART_SET_CONFIG_EXT,         //45
    UART_GET_CONFIG_EXT,
};

enum uart_camera_status {
    UART_CAMERA_STATUS_UNKNOWN,
    UART_CAMERA_STATUS_REC_MODE = 0x10,
    UART_CAMERA_STATUS_RECORDING,
    UART_CAMERA_STATUS_PB_MODE = 0x20,
    UART_CAMERA_STATUS_PLAYING,
    UART_CAMERA_STATUS_PB_PAUSED,
    UART_CAMERA_STATUS_STILL_MODE = 0x40,
    UART_CAMERA_STATUS_STILL_MODE_TIMELAPSE_IDLE,
    UART_CAMERA_STATUS_STILL_MODE_TIMELAPSE_ING
};

typedef enum {
    UART_MULTI_ROLE_UART,
    UART_MULTI_ROLE_PTZ,
    UART_MULTI_ROLE_MUX
} UART_MULTI_ROLE;



enum {
    CAMERA_CONFIG_TYPE_CHOICE   = 0x1,
    CAMERA_CONFIG_TYPE_RANGE    = 0x2,
    CAMERA_CONFIG_TYPE_STRING   = 0x3,
};


/* configuration */
enum {
    CAMERA_CONFIG_MOVIE_FORMAT = 0x0,
    CAMERA_CONFIG_PHOTO_SIZE,
    CAMERA_CONFIG_WB,
    CAMERA_CONFIG_ISO,
    CAMERA_CONFIG_SHARPNESS,
    CAMERA_CONFIG_CONTRAST,
    CAMERA_CONFIG_AE_METER_MODE,
    CAMERA_CONFIG_SCENCE,
    CAMERA_CONFIG_DIGITAL_EFFECT,
    CAMERA_CONFIG_FLICKER_REDUCTION,
    CAMERA_CONFIG_VIDEO_SYSTEM,         // 10
    CAMERA_CONFIG_WIFI_ONOFF,
    CAMERA_CONFIG_EV_BIAS,
    CAMERA_CONFIG_BATTERY,
    CAMERA_CONFIG_SATURATION,
    CAMERA_CONFIG_BRIGHTNESS,           // 15
    CAMERA_CONFIG_NOISE_REDUCTION,
    CAMERA_CONFIG_PHOTO_QUALITY,
    CAMERA_CONFIG_LCD_ONOFF,
    CAMERA_CONFIG_ROTATION,
    CAMERA_CONFIG_VERSION,              // 20
    CAMERA_CONFIG_IRIS,
    CAMERA_CONFIG_FOCUS_METHOD, //AF, MF
    CAMERA_CONFIG_AF_AREA,
    CAMERA_CONFIG_MAGNIFY_POSITION,
    CAMERA_CONFIG_NEW_FW,               // 25
    CAMERA_CONFIG_HW_VERSION,
    CAMERA_CONFIG_DO_AF,
    CAMERA_CONFIG_CAF_ONOFF,
    CAMERA_CONFIG_LENS_ATTACHED,
    CAMERA_CONFIG_LED_ENABLE,           // 30
    CAMERA_CONFIG_BEEPER_ENABLE,
    CAMERA_CONFIG_AF_MODE,
    CAMERA_CONFIG_MF_DRIVE,
    CAMERA_CONFIG_MODEL_NAME,
    CAMERA_CONFIG_LCD_BACKLIGHT_LEVEL,  // 35
    CAMERA_CONFIG_PHOTO_BURST,
    CAMERA_CONFIG_RTC_TIME,
    CAMERA_CONFIG_BT_MAC,
    CAMERA_CONFIG_MAX_SHUTTER_SPEED,
    CAMERA_CONFIG_PC_CONNECTED,         // 40
    CAMERA_CONFIG_USB_CABLE_STATUS,
    CAMERA_CONFIG_OLED_ONOFF_ENABLE,
    CAMERA_CONFIG_SHUTTER_ANGLE,
    CAMERA_CONFIG_DCF_REACH_MAX_NUMBER,
    CAMERA_CONFIG_MANUAL_WB,            // 45
    CAMERA_CONFIG_HDMI_OSD_ONOFF,
    CAMERA_CONFIG_STILL_SHUTTER_SPEED,
    CAMERA_CONFIG_LENS_ZOOM,
    CAMERA_CONFIG_DCF_FILE_NUMBERING,
    CAMERA_CONFIG_CVBS_VIDEO_SYSTEM,    // 50
    CAMERA_CONFIG_CVBS_OUTPUT_ENABLE,
    CAMERA_CONFIG_LENS_FOCUS_POSITION,
    CAMERA_CONFIG_LENS_FOCUS_SPEED,
    CAMERA_CONFIG_MANUAL_WB_TINT,
    CAMERA_CONFIG_CAF_RANGE,            // 55
    CAMERA_CONFIG_CAF_SENSITIVITY,
    CAMERA_CONFIG_ENC_ROTATION,
    CAMERA_CONFIG_VIDEO_QUALITY,
    CAMERA_CONFIG_DUAL_STREAM_ENABLE,
    CAMERA_CONFIG_PHOTO_AEB,            // 60
    CAMERA_CONFIG_CAPTURE_TIMESTAMP,
    CAMERA_CONFIG_RECORD_TIMESTAMP,
    CAMERA_CONFIG_IMU_ROTATION,
    CAMERA_CONFIG_PHOTO_BURST_SPEED,
    CAMERA_CONFIG_LUT_TYPE,           //65
    CAMERA_CONFIG_DCF_LAST_FILE_NAME,
    CAMERA_CONFIG_UART_COMMAND_SUPPORTED,
    CAMERA_CONFIG_LCD_RUNTIME_ONOFF,
    CAMERA_CONFIG_MOV_CONTAINER_ROTATION,
    CAMERA_CONFIG_UI_TIMELAPSE_STATUS,  // 70, internal use
    CAMERA_CONFIG_USB_CHARGE_DETECTION, //
    CAMERA_CONFIG_USB_DEVICE_ROLE,
    CAMERA_CONFIG_IC_TEMPERATURE,
    CAMERA_CONFIG_DCF_NAME_MODE,// 1 ABCD0001.JPG 2 ABCD_201501011633_0001.JPG 3 ABCD_0001_201501011633.JPG
    CAMERA_CONFIG_CAMERA_IS_MULTIPLE, // 75  // camera is multiple master or slave
    CAMERA_CONFIG_DEWARP_ONOFF, //76
    CAMERA_CONFIG_MAX_RECORD_TEMPERATURE_LIMIT,
    CAMERA_CONFIG_VIGNETTE_ONOFF,    //// vignette correction
    CAMERA_CONFIG_SECONDARY_STREAM_RESOLUTION,
    CAMERA_CONFIG_SECONDARY_STREAM_BITRATE,  // 80
    CAMERA_CONFIG_RECORD_INT_CAP,
    CAMERA_CONFIG_HDMI_PREFER_FORMAT,
    CAMERA_CONFIG_MULTIPLE_CONTROL_ID,
    CAMERA_CONFIG_MULTIPLE_CAPTURE_DELAY,
    CAMERA_CONFIG_CAMERA_DEFLECTION_ANGLE,   // 85
    CAMERA_CONFIG_VOLUME_CONTROL,
    CAMERA_CONFIG_AE_EXPOSURE_MDOE,
    CAMERA_CONFIG_OIS_MODE,
    CAMERA_CONFIG_MOVIE_RECORD_DURATION,
    CAMERA_CONFIG_MULTIPLE_TIMEOUT_ENABLE,   // 90
    CAMERA_CONFIG_MULTIPLE_CONTROL_ENABLE,
    CAMERA_CONFIG_AEB_NUMCAPTURE,
    CAMERA_CONFIG_LIVEVIEW_WITH_AUDIO,
    CAMERA_CONFIG_SECONDARY_AUDIO_TYPE,
    CAMERA_CONFIG_VIDEO_ENCODER,     // 95
    CAMERA_CONFIG_MAX_ISO_LIMIT,
    CAMERA_CONFIG_SEND_STREAM,
    CAMERA_CONFIG_UNION_AE,
    CAMERA_CONFIG_UNION_AWB,
    CAMERA_CONFIG_VIDEO_SHUTTER_TIME,   // 100
    CAMERA_CONFIG_PRODUCT_SN,
    CAMERA_CONFIG_GET_IS_SUPPORT_DUAL_STREAM,
    CAMERA_CONFIG_UNION_AE_DELTA,
    CAMERA_CONFIG_UNION_AWB_DELTA,
    CAMERA_CONFIG_UNION_AE_PRIORITY,    // 105
    CAMERA_CONFIG_WB_CALIB,
    CAMERA_CONFIG_UNION_AWB_PRIORITY,
    CAMERA_CONFIG_LIVE_AE_INFO_FNO,
    CAMERA_CONFIG_LIVE_AE_INFO_ISO,
    CAMERA_CONFIG_LIVE_AE_INFO_SHUTTER,  // 110
    CAMERA_CONFIG_NETWORK_MODE,
    CAMERA_CONFIG_GET_NUM_OF_CAMERA,
    CAMERA_CONFIG_CROP_SETTING,
    CAMERA_CONFIG_BITRATE_LEVEL,
    CAMERA_CONFIG_AE_LOCK,              //115
    CAMERA_CONFIG_BLC_CALIB_ADJUST,
    CAMERA_CONFIG_LIVIVIEW_AE_INFO_ISO,
    CAMERA_CONFIG_LIVIVIEW_AE_INFO_SHUTTER,
    CAMERA_CONFIG_RECORD_FILE_FORMAT,
    CAMERA_CONFIG_FAN_MODE_SWITCH,     // 120
    CAMERA_CONFIG_PRIMARY_STREAM_BITRATE,
    CAMERA_CONFIG_PRIMARY_AUDIO_TYPE,
    CAMERA_CONFIG_SECONDARY_B_FRAME,
    CAMERA_CONFIG_SECONDARY_STREAM_BITRATE_TYPE,
    CAMERA_CONFIG_SECONDRY_STREAM_GOP, // 125
    CAMERA_CONFIG_WB_PRIORITY,
    CAMERA_CONFIG_DRIVE_MODE,
    CAMERA_CONFIG_SHUTTER_UNIT,
    CAMERA_CONFIG_DUAL_NATIVE_ISO_MODE,
    CAMERA_CONFIG_ACODEC_INPUT_CHANNEL, // 130
    CAMERA_CONFIG_LIVE_AE_INFO_SHUTTER_ANGLE,
    CAMERA_CONFIG_AE_FREEZE,
    CAMERA_CONFIG_AF_LOCK,
    CAMERA_CONFIG_GAMMA,
    CAMERA_CONFIG_CLUT,               // 135
    CAMERA_CONFIG_LVDS_CROP_SETTING,
    CAMERA_CONFIG_LENS_ZOOM_POSITION,
    CAMERA_CONFIG_LUMA_LEVEL,
    CAMERA_CONFIG_EV, // ui value
    CAMERA_CONFIG_MOVIE_VFR,                  // 140
    CAMERA_CONFIG_ASSITOOL_DISPLAY,
    CAMERA_CONFIG_ASSITOOL_PEAK_ONOFF,
    CAMERA_CONFIG_ASSITOOL_PEAK_COLOR,
    CAMERA_CONFIG_ASSITOOL_EXPOSURE_TOOL,
    CAMERA_CONFIG_ASSITOOL_ZEBRA_TH1,    // 145
    CAMERA_CONFIG_ASSITOOL_ZEBRA_TH2,
    CAMERA_CONFIG_MAX_EXPOSURE_SHR_ANGLE,
    CAMERA_CONFIG_MAX_EXPOSURE_SHR_TIME,
    CAMERA_CONFIG_RECORD_FRAMERTAE,
    CAMERA_CONFIG_DESQUEEZE_FACTOR,     // 150
    CAMERA_CONFIG_LIVE_CAF,
    CAMERA_CONFIG_WB_FREEZE,
    CAMERA_CONFIG_WB_MWB_AUTO_DETECT,
    CAMERA_CONFIG_MIN_ISO_LIMIT,
    CAMERA_CONFIG_ASSITOOL_OVERLAY_FRAME_LINE,  //155
    CAMERA_CONFIG_ASSITOOL_OVERLAY_CENTER_MARK,
    CAMERA_CONFIG_MOVIE_RESOLUTION,
    CAMERA_CONFIG_MOVIE_PROJECT_FPS,
    CAMERA_CONFIG_ASSITOOL_FRAME_LINE_COLOR,
    CAMERA_CONFIG_ASSITOOL_CENTER_MARK_COLOR,   // 160
    CAMERA_CONFIG_OOTF,
    CAMERA_CONFIG_X_MWB_RGAIN,
    CAMERA_CONFIG_X_MWB_GGAIN,
    CAMERA_CONFIG_X_MWB_BGAIN,
    CAMERA_CONFIG_EXTEND_VIDEO_SHUTTER_TIME,    // 165
    CAMERA_CONFIG_META_CAMERA_ID,
    CAMERA_CONFIG_META_REELNAME,
    CAMERA_CONFIG_NP_BATTERY_THRESHOLD,
    CAMERA_CONFIG_VMOUNT_BATTERY_THRESHOLD,
    CAMERA_CONFIG_BATTERY_VOLTAGE,              // 170
    CAMERA_CONFIG_VFR_CONTROL_TYPE,
    CAMERA_CONFIG_FILELIST_ENABLE,
    CAMERA_CONFIG_PRERECORD_ENABLE,
    CAMERA_CONFIG_ASSITOOL_SCOPE_TOOL,
    CAMERA_CONFIG_ASSITOOL_SCOPE_OPACITY,          // 175
    CAMERA_CONFIG_ASSITOOL_PEAK_BW_BACKGROUND,
    CAMERA_CONFIG_ASSITOOL_PEAK_THD,
    CAMERA_CONFIG_COLOR_LUT,
    CAMERA_CONFIG_ISO_OPTION_CTRL,
    CAMERA_CONFIG_ND_STOP,                          //180
    CAMERA_CONFIG_ENABLE_CROP_SENSOR,
    CAMERA_CONFIG_AE_SPEED_RATIO,
    CAMERA_CONFIG_HDMI_USE_EDID,


    ///////////////////////////////////////////////////////////
    // move from A9 local config
    CAMERA_CONFIG_AUTO_OFF = 0x100,          // 256
    CAMERA_CONFIG_PHOTO_TIMELAPSE_INTERVAL,
    CAMERA_CONFIG_PHOTO_TIMELAPSE_NUM,
    CAMERA_CONFIG_PHOTO_SELF_TIMER_INTERVAL,
    CAMERA_CONFIG_AUTO_OFF_LCD, // 260
    CAMERA_CONFIG_GRID_DISPLAY_ONOFF,
    CAMERA_CONFIG_FOCUS_AREA_OPTION,
    CAMERA_CONFIG_LEVEL_CORRECTION_ONOFF,
    CAMERA_CONFIG_RECORD_TIMELAPSE_INTERVAL,
    CAMERA_CONFIG_CAF_ONOFF_CONFIG, // 265 to decide turn on/off CAF in record movie
    CAMERA_CONFIG_FN_KEY_OPTION,
    CAMERA_CONFIG_F2_KEY_OPTION,
    CAMERA_CONFIG_ROTATION_MOVIE_SQUARE_FORMAT,
    CAMERA_CONFIG_PREF_WIFI_MODE,
    CAMERA_CONFIG_ENABLE_VIDEO_TIMELAPSE, // 270
    CAMERA_CONFIG_MULTIPLE_CONTROL_VR_SNAP_ENABLE,
    CAMERA_CONFIG_MULTIPLE_CONTROL_VR_SNAP_INTERVAL,
    CAMERA_CONFIG_MULTIPLE_CONTROL_VR_SNAP_COUNT,
    CAMERA_CONFIG_RECORD_DURATION,
    CAMERA_CONFIG_VR_SNAP_PHOTO_TOKEN, // 275
    CAMERA_CONFIG_FOCUS_MODE, // use CAMERA_CONFIG_FOCUS_METHOD
    CAMERA_CONFIG_COMPOSE_MODE, //WDR
    CAMERA_CONFIG_AUDIO_INPUT_GAIN,
    CAMERA_CONFIG_AUDIO_OUTPUT_GAIN,
    CAMERA_CONFIG_PHOTO_BURST_NUM, // 280
    CAMERA_CONFIG_TIME_CODE_COUNT_UP,
    CAMERA_CONFIG_TIME_CODE_HDMI_DISPALY,
    CAMERA_CONFIG_3D_LUT_TYPE,
    CAMERA_CONFIG_UART_ROLE,
    CAMERA_CONFIG_F1_KEY_OPTION,
    CAMERA_CONFIG_F3_KEY_OPTION,
    CAMERA_CONFIG_F4_KEY_OPTION,
    CAMERA_CONFIG_RECORD_PROXY_FILE_ONOFF,
    CAMERA_CONFIG_TIME_CODE_DROP_FRAME,
    CAMERA_CONFIG_UP_KEY_OPTION,
    CAMERA_CONFIG_DOWN_KEY_OPTION,
    CAMERA_CONFIG_OK_KEY_OPTION,
    CAMERA_CONFIG_LANC,
    CAMERA_CONFIG_RESTORE_LENS_POSITION,
    CAMERA_CONFIG_AUDIO_PHANTOM_POWER,
    CAMERA_CONFIG_MF_ASSIST,
    CAMERA_CONFIG_TIME_CODE_SOURCE,
    CAMERA_CONFIG_MF_ASSIST_PREVIEW,
    CAMERA_CONFIG_MF_ASSIST_RECORDING,
    CAMERA_CONFIG_POWER_KEY_OPTION,
    CAMERA_CONFIG_AUDIO_INPUT_LEVEL_DISPLAY,
    CAMERA_CONFIG_WIFI_CHANNEL,
    CAMERA_CONFIG_POWER_OUTPUT_ONOFF,
    CAMERA_CONFIG_BACK_LED_ENABLE,
    CAMERA_CONFIG_SUPPORT_LINE_IN_INPUT,
    CAMERA_CONFIG_AUDIO_SUPPORT_AGC,

    CAMERA_CONFIG_NONE,
};

#endif
