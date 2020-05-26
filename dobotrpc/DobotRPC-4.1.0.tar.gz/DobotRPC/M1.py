from DobotRPC import DobotlinkAdapter, RPCClient


class M1Api(object):
    def __init__(self):
        self.__port_name: str
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    def set_portname(self, port_name):
        self.__port_name = port_name

    def search_dobot(self):
        return self.__dobotlink.M1.SearchDobot()

    def connect_dobot(self, queue_start=True):
        return self.__dobotlink.M1.ConnectDobot(portName=self.__port_name,
                                                queueStart=queue_start)

    def disconnect_dobot(self, queue_stop=True, queue_clear=True):
        return self.__dobotlink.M1.DisconnectDobot(portName=self.__port_name,
                                                   queueStop=queue_stop,
                                                   queueClear=queue_clear)

    def get_devicesn(self, ):
        return self.__dobotlink.M1.GetDeviceSN(portName=self.__port_name, )

    def set_devicename(self, device_name):
        return self.__dobotlink.M1.SetDeviceName(portName=self.__port_name,
                                                 deviceName=device_name)

    def get_devicename(self, ):
        return self.__dobotlink.M1.GetDeviceName(portName=self.__port_name, )

    def get_deviceversion(self, get_type: int):
        return self.__dobotlink.M1.GetDeviceVersion(portName=self.__port_name,
                                                    type=get_type)

    def get_hardware_version(self, ):
        return self.__dobotlink.M1.GetHardwareVersion(
            portName=self.__port_name, )

    def queuedcmd_start(self, ):
        return self.__dobotlink.M1.QueuedCmdStart(portName=self.__port_name, )

    def queuedcmd_stop(self, force_stop=False):
        return self.__dobotlink.M1.QueuedCmdStop(portName=self.__port_name,
                                                 forceStop=force_stop)

    def queuedcmd_clear(self, ):
        return self.__dobotlink.M1.QueuedCmdClear(portName=self.__port_name, )

    def queuedcmd_startdownload(self, total_loop, lineper_loop):
        return self.__dobotlink.M1.QueuedCmdStartDownload(
            portName=self.__port_name,
            totalLoop=total_loop,
            linePerLoop=lineper_loop)

    def queuedcmd_stopdownload(self, ):
        return self.__dobotlink.M1.QueuedCmdStopDownload(
            portName=self.__port_name, )

    def get_queuedcmd_currentindex(self, ):
        return self.__dobotlink.M1.GetQueuedCmdCurrentIndex(
            portName=self.__port_name, )

    def get_queuedcmd_leftspace(self, ):
        return self.__dobotlink.M1.GetQueuedCmdLeftSpace(
            portName=self.__port_name, )

    def get_pose(self, ):
        return self.__dobotlink.M1.GetPose(portName=self.__port_name, )

    def reset_pose(self, front_angle1, front_angle2):
        return self.__dobotlink.M1.ResetPose(portName=self.__port_name,
                                             frontAngle1=front_angle1,
                                             frontAngle2=front_angle2)

    def set_usercoordinate(self,
                           x: float,
                           y: float,
                           z: float,
                           r: float,
                           is_queued=False):
        return self.__dobotlink.M1.SetUserCoordinate(portName=self.__port_name,
                                                     x=x,
                                                     y=y,
                                                     z=z,
                                                     r=r,
                                                     isQueued=is_queued)

    def get_usercoordinate(self, ):
        return self.__dobotlink.M1.GetUserCoordinate(
            portName=self.__port_name, )

    def set_toolcoordinate(self,
                           x: float,
                           y: float,
                           z: float,
                           r: float,
                           is_queued=False):
        return self.__dobotlink.M1.SetToolCoordinate(portName=self.__port_name,
                                                     x=x,
                                                     y=y,
                                                     z=z,
                                                     r=r,
                                                     isQueued=is_queued)

    def get_toolcoordinate(self, ):
        return self.__dobotlink.M1.GetToolCoordinate(
            portName=self.__port_name, )

    def get_alarms_state(self, ):
        return self.__dobotlink.M1.GetAlarmsState(portName=self.__port_name, )

    def clear_allalarms_state(self, ):
        return self.__dobotlink.M1.ClearAllAlarmsState(
            portName=self.__port_name, )

    def get_run_state(self, ):
        return self.__dobotlink.M1.GetRunState(portName=self.__port_name, )

    def set_homecmd(self,
                    is_resetpars=False,
                    is_queued=True,
                    iswait_forfinish=True,
                    time_out=25000):
        return self.__dobotlink.M1.SetHOMECmd(portName=self.__port_name,
                                              isResetPars=is_resetpars,
                                              isQueued=is_queued,
                                              isWaitForFinish=iswait_forfinish,
                                              timeout=time_out)

    def set_home_initialpos(self, ):
        return self.__dobotlink.M1.SetHOMEInitialPos(
            portName=self.__port_name, )

    def set_hhttrig_mode(self, mode: int, is_queued=False):
        return self.__dobotlink.M1.SetHHTTrigMode(portName=self.__port_name,
                                                  mode=mode,
                                                  isQueued=is_queued)

    def get_hhttrig_mode(self, ):
        return self.__dobotlink.M1.GetHHTTrigMode(portName=self.__port_name, )

    def set_hhttrig_output_enabled(self, enable: bool, is_queued=False):
        return self.__dobotlink.M1.SetHHTTrigOutputEnabled(
            portName=self.__port_name, enable=enable, isQueued=is_queued)

    def get_hhttrig_output_enabled(self, ):
        return self.__dobotlink.M1.GetHHTTrigOutputEnabled(
            portName=self.__port_name, )

    def get_hhttrig_output(self, ):
        return self.__dobotlink.M1.GetHHTTrigOutput(
            portName=self.__port_name, )

    def set_servo_power(self, on: bool, is_queued=False):
        return self.__dobotlink.M1.SetServoPower(portName=self.__port_name,
                                                 on=on,
                                                 isQueued=is_queued)

    def set_endeffector_params(self,
                               x_offset: float,
                               y_offset: float,
                               z_offset: float,
                               is_queued=False):
        return self.__dobotlink.M1.SetEndEffectorParams(
            portName=self.__port_name,
            xOffset=x_offset,
            yOffset=y_offset,
            zOffset=z_offset,
            isQueued=is_queued)

    def get_endeffector_params(self, ):
        return self.__dobotlink.M1.GetEndEffectorParams(
            portName=self.__port_name, )

    def set_endeffector_laser(self, enable: bool, on: bool, is_queued=False):
        return self.__dobotlink.M1.SetEndEffectorLaser(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_laser(self, ):
        return self.__dobotlink.M1.GetEndEffectorLaser(
            portName=self.__port_name, )

    def set_endeffector_suctioncup(self,
                                   enable: bool,
                                   on: bool,
                                   is_queued=False):
        return self.__dobotlink.M1.SetEndEffectorSuctionCup(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_suctioncup(self, ):
        return self.__dobotlink.M1.GetEndEffectorSuctionCup(
            portName=self.__port_name, )

    def set_endeffector_gripper(self, enable: bool, on: bool, is_queued=False):
        return self.__dobotlink.M1.SetEndEffectorGripper(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_gripper(self, ):
        return self.__dobotlink.M1.GetEndEffectorGripper(
            portName=self.__port_name, )

    def set_jogjoint_params(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.M1.SetJOGJointParams(portName=self.__port_name,
                                                     velocity=velocity,
                                                     acceleration=acceleration,
                                                     isQueued=is_queued)

    def get_jogjoint_params(self, ):
        return self.__dobotlink.M1.GetJOGJointParams(
            portName=self.__port_name, )

    def set_jogcoordinate_params(self,
                                 velocity,
                                 acceleration,
                                 is_queued=False):
        return self.__dobotlink.M1.SetJOGCoordinateParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_jogcoordinate_params(self, ):
        return self.__dobotlink.M1.GetJOGCoordinateParams(
            portName=self.__port_name, )

    def set_jogcommon_params(self,
                             velocity_ratio,
                             acceleration_ratio,
                             is_queued=False):
        return self.__dobotlink.M1.SetJOGCommonParams(
            portName=self.__port_name,
            velocityRatio=velocity_ratio,
            accelerationRatio=acceleration_ratio,
            isQueued=is_queued)

    def get_jogcommon_params(self, ):
        return self.__dobotlink.M1.GetJOGCommonParams(
            portName=self.__port_name, )

    def set_jogcmd(self, is_joint, cmd, is_queued):
        return self.__dobotlink.M1.SetJOGCmd(portName=self.__port_name,
                                             isJoint=is_joint,
                                             cmd=cmd,
                                             isQueued=is_queued)

    def set_inchmode(self, mode: int):
        return self.__dobotlink.M1.SetInchMode(portName=self.__port_name,
                                               mode=mode)

    def get_inchmode(self, ):
        return self.__dobotlink.M1.GetInchMode(portName=self.__port_name, )

    def set_inchparam(self, distance_mm: float, distance_ang: float):
        return self.__dobotlink.M1.SetInchParam(portName=self.__port_name,
                                                distanceMM=distance_mm,
                                                distanceANG=distance_ang)

    def get_inchparam(self, ):
        return self.__dobotlink.M1.GetInchParam(portName=self.__port_name, )

    def set_ptpcmd(self,
                   ptp_mode,
                   x,
                   y,
                   z,
                   r,
                   is_queued=True,
                   iswait_forfinish=True):
        return self.__dobotlink.M1.SetPTPCmd(portName=self.__port_name,
                                             ptpMode=ptp_mode,
                                             x=x,
                                             y=y,
                                             z=z,
                                             r=r,
                                             isQueued=is_queued,
                                             isWaitForFinish=iswait_forfinish)

    def set_ptpjoint_param(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.M1.SetPTPJointParams(portName=self.__port_name,
                                                     velocity=velocity,
                                                     acceleration=acceleration,
                                                     isQueued=is_queued)

    def get_ptpjoint_param(self, ):
        return self.__dobotlink.M1.GetPTPJointParams(
            portName=self.__port_name, )

    def set_ptpcoordinate_params(self,
                                 xyz_velocity,
                                 r_velocity,
                                 xyz_acceleration,
                                 r_acceleration,
                                 is_queued=False):
        return self.__dobotlink.M1.SetPTPCoordinateParams(
            portName=self.__port_name,
            xyzVelocity=xyz_velocity,
            rVelocity=r_velocity,
            xyzAcceleration=xyz_acceleration,
            rAcceleration=r_acceleration,
            isQueued=is_queued)

    def get_ptpcoordinate_params(self, ):
        return self.__dobotlink.M1.GetPTPCoordinateParams(
            portName=self.__port_name, )

    def set_ptpjump_params(self,
                           isusing_zlimit,
                           z_limit,
                           jump_height,
                           is_queued=False):
        return self.__dobotlink.M1.SetPTPJumpParams(
            portName=self.__port_name,
            isUsingZLimit=isusing_zlimit,
            zLimit=z_limit,
            jumpHeight=jump_height,
            isQueued=is_queued)

    def get_ptpjump_params(self, ):
        return self.__dobotlink.M1.GetPTPJumpParams(
            portName=self.__port_name, )

    def set_ptpcommon_params(self,
                             velocity_ratio,
                             acceleration_ratio,
                             is_queued=False):
        return self.__dobotlink.M1.SetPTPCommonParams(
            portName=self.__port_name,
            velocityRatio=velocity_ratio,
            accelerationRatio=acceleration_ratio,
            isQueued=is_queued)

    def get_ptpcommon_params(self, ):
        return self.__dobotlink.M1.GetPTPCommonParams(
            portName=self.__port_name, )

    def set_motivation_mode(self, mode: int):
        return self.__dobotlink.M1.SetMotivationMode(portName=self.__port_name,
                                                     mode=mode)

    def get_motivation_mode(self, ):
        return self.__dobotlink.M1.GetMotivationMode(
            portName=self.__port_name, )

    def set_motivate_cmd(self,
                         q1,
                         q2,
                         dq1,
                         dq2,
                         ddq1,
                         ddq2,
                         is_queued: bool,
                         iswait_forfinish,
                         time_out=10000):
        return self.__dobotlink.M1.SetMotivateCmd(
            portName=self.__port_name,
            q1=q1,
            q2=q2,
            dq1=dq1,
            dq2=dq2,
            ddq1=ddq1,
            ddq2=ddq2,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    def set_motivate_zcmd(self, qz, dqz, ddqz, is_queued: bool,
                          iswait_forfinish):
        return self.__dobotlink.M1.SetMotivateZCmd(
            portName=self.__port_name,
            qz=qz,
            dqz=dqz,
            ddqz=ddqz,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish)

    def get_trajectory(self, count_max, index):
        return self.__dobotlink.M1.GetTrajectory(portName=self.__port_name,
                                                 countMax=count_max,
                                                 index=index)

    def set_iodo(self, port, level, is_queued=False):
        return self.__dobotlink.M1.SetIODO(portName=self.__port_name,
                                           port=port,
                                           level=level,
                                           isQueued=is_queued)

    def get_iodo(self, port):
        return self.__dobotlink.M1.GetIODO(portName=self.__port_name,
                                           port=port)

    def get_iodi(self, port):
        return self.__dobotlink.M1.GetIODI(portName=self.__port_name,
                                           port=port)

    def get_ioadc(self, port):
        return self.__dobotlink.M1.GetIOADC(portName=self.__port_name,
                                            port=port)

    def set_cpparams(self,
                     target_acc,
                     junction_vel,
                     isreal_timetrack,
                     acc=None,
                     period=None,
                     is_queued=False):
        return self.__dobotlink.M1.SetCPParams(
            portName=self.__port_name,
            targetAcc=target_acc,
            junctionVel=junction_vel,
            isRealTimeTrack=isreal_timetrack,
            acc=acc,
            period=period,
            isQueued=is_queued)

    def get_cpparams(self, ):
        return self.__dobotlink.M1.GetCPParams(portName=self.__port_name, )

    def set_cpcmd(self, cp_mode, x, y, z, power, is_queued=False):
        return self.__dobotlink.M1.SetCPCmd(portName=self.__port_name,
                                            cpMode=cp_mode,
                                            x=x,
                                            y=y,
                                            z=z,
                                            power=power,
                                            isQueued=is_queued)

    def set_cplecmd(self, cp_mode, x, y, z, power, is_queued=False):
        return self.__dobotlink.M1.SetCPLECmd(portName=self.__port_name,
                                              cpMode=cp_mode,
                                              x=x,
                                              y=y,
                                              z=z,
                                              power=power,
                                              isQueued=is_queued)

    def set_arcparams(self,
                      xyz_velocity,
                      r_velocity,
                      xyz_acceleration,
                      r_acceleration,
                      is_queued=False):
        return self.__dobotlink.M1.SetARCParams(
            portName=self.__port_name,
            xyzVelocity=xyz_velocity,
            rVelocity=r_velocity,
            xyzAcceleration=xyz_acceleration,
            rAcceleration=r_acceleration,
            isQueued=is_queued)

    def get_arcparams(self, ):
        return self.__dobotlink.M1.GetARCParams(portName=self.__port_name, )

    def set_arccmd(self, cir_point, to_point, is_queued=False):
        return self.__dobotlink.M1.SetARCCmd(portName=self.__port_name,
                                             cirPoint=cir_point,
                                             toPoint=to_point,
                                             isQueued=is_queued)

    def set_arcpocmd(self, cir_point, to_point, arc_po, is_queued=False):
        return self.__dobotlink.M1.SetARCPOCmd(portName=self.__port_name,
                                               cirPoint=cir_point,
                                               toPoint=to_point,
                                               arcPO=arc_po,
                                               isQueued=is_queued)

    def set_circle_cmd(self,
                       cir_point,
                       to_point,
                       count,
                       is_queued=False,
                       iswait_forfinish=True,
                       time_out=60000):
        return self.__dobotlink.M1.SetCircleCmd(
            portName=self.__port_name,
            cirPoint=cir_point,
            toPoint=to_point,
            count=count,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    def set_circle_pocmd(self,
                         cir_point,
                         to_point,
                         count,
                         circle_po,
                         is_queued=False):
        return self.__dobotlink.M1.SetCirclePOCmd(portName=self.__port_name,
                                                  cirPoint=cir_point,
                                                  toPoint=to_point,
                                                  count=count,
                                                  circlePO=circle_po,
                                                  isQueued=is_queued)

    def set_arm_orientation(self, arm_orientation):
        return self.__dobotlink.M1.SetArmOrientation(
            portName=self.__port_name, armOrientation=arm_orientation)

    def get_arm_orientation(self, ):
        return self.__dobotlink.M1.GetArmOrientation(
            portName=self.__port_name, )

    def set_waitcmd(self, time_out: int, is_queued=False):
        return self.__dobotlink.M1.SetWAITCmd(portName=self.__port_name,
                                              timeout=time_out,
                                              isQueued=is_queued)

    def set_safemode_enabled(self, enable):
        return self.__dobotlink.M1.SetSafeModeEnabled(
            portName=self.__port_name, enable=enable)

    def get_safemode_enabled(self, ):
        return self.__dobotlink.M1.GetSafeModeEnabled(
            portName=self.__port_name, )

    def set_collision_threshold(self, tor_diffj1, tor_diffj2, tor_diffj3,
                                tor_diffj4):
        return self.__dobotlink.M1.SetCollisionThreshold(
            portName=self.__port_name,
            torDiffJ1=tor_diffj1,
            torDiffJ2=tor_diffj2,
            torDiffJ3=tor_diffj3,
            torDiffJ4=tor_diffj4)

    def get_collision_threshold(self, ):
        return self.__dobotlink.M1.GetCollisionThreshold(
            portName=self.__port_name, )

    def set_basicdynamic_params(self, zz1, fs1, fv1, zz2, mx2, my2, ia2, fs2,
                                fv2):
        return self.__dobotlink.M1.SetBasicDynamicParams(
            portName=self.__port_name,
            ZZ1=zz1,
            FS1=fs1,
            FV1=fv1,
            ZZ2=zz2,
            MX2=mx2,
            MY2=my2,
            IA2=ia2,
            FS2=fs2,
            FV2=fv2)

    def get_basicdynamic_params(self, ):
        return self.__dobotlink.M1.GetBasicDynamicParams(
            portName=self.__port_name, )

    def set_load_params(self, load_params):
        return self.__dobotlink.M1.SetLoadParams(portName=self.__port_name,
                                                 loadParams=load_params)

    def get_load_params(self, ):
        return self.__dobotlink.M1.GetLoadParams(portName=self.__port_name, )

    def set_safestrategy(self, strategy):
        return self.__dobotlink.M1.SetSafeStrategy(portName=self.__port_name,
                                                   strategy=strategy)

    def get_safestrategy(self, ):
        return self.__dobotlink.M1.GetSafeStrategy(portName=self.__port_name, )

    def set_safeguard_mode(self, mode):
        return self.__dobotlink.M1.SetSafeGuardMode(portName=self.__port_name,
                                                    mode=mode)

    def get_safeguard_mode(self, ):
        return self.__dobotlink.M1.GetSafeGuardMode(
            portName=self.__port_name, )

    def get_safeguard_status(self, ):
        return self.__dobotlink.M1.GetSafeGuardStatus(
            portName=self.__port_name, )

    def set_lanport_config(self, addr, mask, gateway, dns, isdhcp):
        return self.__dobotlink.M1.SetLanPortConfig(portName=self.__port_name,
                                                    addr=addr,
                                                    mask=mask,
                                                    gateway=gateway,
                                                    dns=dns,
                                                    isdhcp=isdhcp)

    def get_lanport_config(self, ):
        return self.__dobotlink.M1.GetLanPortConfig(
            portName=self.__port_name, )

    def set_firmware_reboot(self, ):
        return self.__dobotlink.M1.SetFirmwareReboot(
            portName=self.__port_name, )

    def set_firmware_notifym4mode(self, mode):
        return self.__dobotlink.M1.SetFirmwareNotifyM4Mode(
            portName=self.__port_name, mode=mode)

    def get_firmware_notifym4mode(self, ):
        return self.__dobotlink.M1.GetFirmwareNotifyM4Mode(
            portName=self.__port_name, )

    def set_feed_forward(self, value):
        return self.__dobotlink.M1.SetFeedforward(portName=self.__port_name,
                                                  value=value)

    def get_feed_forward(self, ):
        return self.__dobotlink.M1.GetFeedforward(portName=self.__port_name, )
