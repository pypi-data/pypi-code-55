from DobotRPC import DobotlinkAdapter, RPCClient


class LiteApi(object):
    def __init__(self):
        self.__port_name: str
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    def set_portname(self, port_name):
        self.__port_name = port_name

    def search_dobot(self):
        return self.__dobotlink.MagicianLite.SearchDobot()

    def connect_dobot(self, queue_start=True):
        return self.__dobotlink.MagicianLite.ConnectDobot(
            portName=self.__port_name, queueStart=queue_start)

    def disconnect_dobot(self, queue_stop=True, queue_clear=True):
        return self.__dobotlink.MagicianLite.DisconnectDobot(
            portName=self.__port_name,
            queueStop=queue_stop,
            queueClear=queue_clear)

    def get_devicesn(self):
        return self.__dobotlink.MagicianLite.GetDeviceSN(
            portName=self.__port_name)

    def set_devicename(self, device_name):
        return self.__dobotlink.MagicianLite.SetDeviceName(
            portName=self.__port_name, deviceName=device_name)

    def get_devicename(self):
        return self.__dobotlink.MagicianLite.GetDeviceName(
            portName=self.__port_name)

    def get_deviceversion(self):
        return self.__dobotlink.MagicianLite.GetDeviceVersion(
            portName=self.__port_name)

    def get_devicetime(self):
        return self.__dobotlink.MagicianLite.GetDeviceTime(
            portName=self.__port_name)

    def get_deviceid(self):
        return self.__dobotlink.MagicianLite.GetDeviceID(
            portName=self.__port_name)

    def get_productname(self):
        return self.__dobotlink.MagicianLite.GetProductName(
            portName=self.__port_name)

    def queuedcmd_start(self):
        return self.__dobotlink.MagicianLite.QueuedCmdStart(
            portName=self.__port_name)

    def queuedcmd_stop(self, force_stop=False):
        return self.__dobotlink.MagicianLite.QueuedCmdStop(
            portName=self.__port_name, forceStop=force_stop)

    def queuedcmd_clear(self):
        return self.__dobotlink.MagicianLite.QueuedCmdClear(
            portName=self.__port_name)

    def queuedcmd_startdownload(self, total_loop, lineper_loop):
        return self.__dobotlink.MagicianLite.QueuedCmdStartDownload(
            portName=self.__port_name,
            totalLoop=total_loop,
            linePerLoop=lineper_loop)

    def queuedcmd_stopdownload(self):
        return self.__dobotlink.MagicianLite.QueuedCmdStopDownload(
            portName=self.__port_name)

    def get_queuedcmd_currentindex(self):
        return self.__dobotlink.MagicianLite.GetQueuedCmdCurrentIndex(
            portName=self.__port_name)

    def get_queuedcmd_leftspace(self):
        return self.__dobotlink.MagicianLite.GetQueuedCmdLeftSpace(
            portName=self.__port_name)

    def set_armspeed_ratio(self,
                           set_type: int,
                           set_value: int,
                           is_queued=False):
        return self.__dobotlink.MagicianLite.SetArmSpeedRatio(
            portName=self.__port_name,
            type=set_type,
            value=set_value,
            isQueued=is_queued)

    def get_armspeed_ratio(self, get_type: int):
        return self.__dobotlink.MagicianLite.GetArmSpeedRatio(
            portName=self.__port_name, type=get_type)

    def get_pose(self):
        return self.__dobotlink.MagicianLite.GetPose(portName=self.__port_name)

    def reset_pose(self,
                   manual_enable,
                   rear_armangle=None,
                   front_armangle=None):
        return self.__dobotlink.MagicianLite.ResetPose(
            portName=self.__port_name,
            manualEnable=manual_enable,
            rearArmAngle=rear_armangle,
            frontArmAngle=front_armangle)

    def check_poselimit(self, is_joint, x, y, z, r):
        return self.__dobotlink.MagicianLite.CheckPoseLimit(
            portName=self.__port_name, isJoint=is_joint, x=x, y=y, z=z, r=r)

    def get_alarms_state(self):
        return self.__dobotlink.MagicianLite.GetAlarmsState(
            portName=self.__port_name)

    def clear_allalarms_state(self):
        return self.__dobotlink.MagicianLite.ClearAllAlarmsState(
            portName=self.__port_name)

    def set_homeparams(self,
                       x: float,
                       y: float,
                       z: float,
                       r: float,
                       is_queued=False):
        return self.__dobotlink.MagicianLite.SetHOMEParams(
            portName=self.__port_name, x=x, y=y, z=z, r=r, isQueued=is_queued)

    def get_homeparams(self):
        return self.__dobotlink.MagicianLite.GetHOMEParams(
            portName=self.__port_name)

    def set_homecmd(self,
                    is_queued=True,
                    iswait_forfinish=True,
                    time_out=25000):
        return self.__dobotlink.MagicianLite.SetHOMECmd(
            portName=self.__port_name,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    def set_endeffector_params(self,
                               x_offset: float,
                               y_offset: float,
                               z_offset: float,
                               is_queued=False):
        return self.__dobotlink.MagicianLite.SetEndEffectorParams(
            portName=self.__port_name,
            xOffset=x_offset,
            yOffset=y_offset,
            zOffset=z_offset,
            isQueued=is_queued)

    def get_endeffector_params(self):
        return self.__dobotlink.MagicianLite.GetEndEffectorParams(
            portName=self.__port_name)

    def set_endeffector_type(self, set_type: int, is_queued=False):
        return self.__dobotlink.MagicianLite.SetEndEffectorType(
            portName=self.__port_name, type=set_type, isQueued=is_queued)

    def get_endeffector_type(self):
        return self.__dobotlink.MagicianLite.GetEndEffectorType(
            portName=self.__port_name)

    def set_endeffector_suctioncup(self,
                                   enable: bool,
                                   on: bool,
                                   is_queued=False):
        return self.__dobotlink.MagicianLite.SetEndEffectorSuctionCup(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_suctioncup(self):
        return self.__dobotlink.MagicianLite.GetEndEffectorSuctionCup(
            portName=self.__port_name)

    def set_endeffector_gripper(self, enable: bool, on: bool, is_queued=False):
        return self.__dobotlink.MagicianLite.SetEndEffectorGripper(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_gripper(self):
        return self.__dobotlink.MagicianLite.GetEndEffectorGripper(
            portName=self.__port_name)

    def set_jogjoint_params(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.MagicianLite.SetJOGJointParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_jogjoint_params(self):
        return self.__dobotlink.MagicianLite.GetJOGJointParams(
            portName=self.__port_name)

    def set_jogcoordinate_params(self,
                                 velocity,
                                 acceleration,
                                 is_queued=False):
        return self.__dobotlink.MagicianLite.SetJOGCoordinateParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_jogcoordinate_params(self):
        return self.__dobotlink.MagicianLite.GetJOGCoordinateParams(
            portName=self.__port_name)

    def set_jogcommon_params(self,
                             velocity_ratio,
                             acceleration_ratio,
                             is_queued=False):
        return self.__dobotlink.MagicianLite.SetJOGCommonParams(
            portName=self.__port_name,
            velocityRatio=velocity_ratio,
            accelerationRatio=acceleration_ratio,
            isQueued=is_queued)

    def get_jogcommon_params(self):
        return self.__dobotlink.MagicianLite.GetJOGCommonParams(
            portName=self.__port_name)

    def set_jogcmd(self, is_joint, cmd, is_queued):
        return self.__dobotlink.MagicianLite.SetJOGCmd(
            portName=self.__port_name,
            isJoint=is_joint,
            cmd=cmd,
            isQueued=is_queued)

    def set_ptpcmd(self,
                   ptp_mode,
                   x,
                   y,
                   z,
                   r,
                   is_queued=True,
                   iswait_forfinish=True):
        return self.__dobotlink.MagicianLite.SetPTPCmd(
            portName=self.__port_name,
            ptpMode=ptp_mode,
            x=x,
            y=y,
            z=z,
            r=r,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish)

    def set_rcmd(self,
                 r: int,
                 is_queued=True,
                 iswait_forfinish=True,
                 time_out=5000):
        return self.__dobotlink.MagicianLite.SetRCmd(
            portName=self.__port_name,
            r=r,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    def set_ptpjoint_param(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.MagicianLite.SetPTPJointParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_ptpjoint_param(self):
        return self.__dobotlink.MagicianLite.GetPTPJointParams(
            portName=self.__port_name)

    def set_ptpcoordinate_params(self,
                                 xyz_velocity,
                                 r_velocity,
                                 xyz_acceleration,
                                 r_acceleration,
                                 is_queued=False):
        return self.__dobotlink.MagicianLite.SetPTPCoordinateParams(
            portName=self.__port_name,
            xyzVelocity=xyz_velocity,
            rVelocity=r_velocity,
            xyzAcceleration=xyz_acceleration,
            rAcceleration=r_acceleration,
            isQueued=is_queued)

    def get_ptpcoordinate_params(self):
        return self.__dobotlink.MagicianLite.GetPTPCoordinateParams(
            portName=self.__port_name)

    def set_ptpjump_params(self, z_limit, jump_height, is_queued=False):
        return self.__dobotlink.MagicianLite.SetPTPJumpParams(
            portName=self.__port_name,
            zLimit=z_limit,
            jumpHeight=jump_height,
            isQueued=is_queued)

    def get_ptpjump_params(self):
        return self.__dobotlink.MagicianLite.GetPTPJumpParams(
            portName=self.__port_name)

    def set_ptpcommon_params(self,
                             velocity_ratio,
                             acceleration_ratio,
                             is_queued=False):
        return self.__dobotlink.MagicianLite.SetPTPCommonParams(
            portName=self.__port_name,
            velocityRatio=velocity_ratio,
            accelerationRatio=acceleration_ratio,
            isQueued=is_queued)

    def get_ptpcommon_params(self):
        return self.__dobotlink.MagicianLite.GetPTPCommonParams(
            portName=self.__port_name)

    def set_loststep_value(self, value):
        return self.__dobotlink.MagicianLite.SetLostStepValue(
            portName=self.__port_name, value=value)

    def set_loststep_cmd(self, is_queued=False):
        return self.__dobotlink.MagicianLite.SetLostStepCmd(
            portName=self.__port_name, isQueued=is_queued)

    def set_collision_check(self, enable, thre_shold):
        return self.__dobotlink.MagicianLite.SetCollisionCheck(
            portName=self.__port_name, enable=enable, threshold=thre_shold)

    def get_collision_check(self, is_queued=False):
        return self.__dobotlink.MagicianLite.GetCollisionCheck(
            portName=self.__port_name)

    def set_cpparams(self,
                     target_acc,
                     junction_vel,
                     isreal_timetrack,
                     acc=None,
                     period=None,
                     is_queued=False):
        return self.__dobotlink.MagicianLite.SetCPParams(
            portName=self.__port_name,
            targetAcc=target_acc,
            junctionVel=junction_vel,
            isRealTimeTrack=isreal_timetrack,
            acc=acc,
            period=period,
            isQueued=is_queued)

    def get_cpparams(self):
        return self.__dobotlink.MagicianLite.GetCPParams(
            portName=self.__port_name)

    def set_cpcmd(self, cp_mode, x, y, z, power, is_queued=False):
        return self.__dobotlink.MagicianLite.SetCPCmd(
            portName=self.__port_name,
            cpMode=cp_mode,
            x=x,
            y=y,
            z=z,
            power=power,
            isQueued=is_queued)

    def set_cplecmd(self, cp_mode, x, y, z, power, is_queued=False):
        return self.__dobotlink.MagicianLite.SetCPLECmd(
            portName=self.__port_name,
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
        return self.__dobotlink.MagicianLite.SetARCParams(
            portName=self.__port_name,
            xyzVelocity=xyz_velocity,
            rVelocity=r_velocity,
            xyzAcceleration=xyz_acceleration,
            rAcceleration=r_acceleration,
            isQueued=is_queued)

    def get_arcparams(self):
        return self.__dobotlink.MagicianLite.GetARCParams(
            portName=self.__port_name)

    def set_arccmd(self, cir_point, to_point, is_queued=False):
        return self.__dobotlink.MagicianLite.SetARCCmd(
            portName=self.__port_name,
            cirPoint=cir_point,
            toPoint=to_point,
            isQueued=is_queued)
