from DobotRPC import DobotlinkAdapter, RPCClient


class MagicianApi(object):
    def __init__(self):
        self.__port_name: str
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    def set_portname(self, port_name):
        self.__port_name = port_name

    def search_dobot(self):
        return self.__dobotlink.Magician.SearchDobot()

    def connect_dobot(self, queue_start=True):
        return self.__dobotlink.Magician.ConnectDobot(
            portName=self.__port_name, queueStart=queue_start)

    def disconnect_dobot(self, queue_stop=True, queue_clear=True):
        return self.__dobotlink.Magician.DisconnectDobot(
            portName=self.__port_name,
            queueStop=queue_stop,
            queueClear=queue_clear)

    def get_devicesn(self):
        return self.__dobotlink.Magician.GetDeviceSN(portName=self.__port_name)

    def set_devicename(self, device_name):
        return self.__dobotlink.Magician.SetDeviceName(
            portName=self.__port_name, deviceName=device_name)

    def get_devicename(self):
        return self.__dobotlink.Magician.GetDeviceName(
            portName=self.__port_name)

    def get_deviceversion(self):
        return self.__dobotlink.Magician.GetDeviceVersion(
            portName=self.__port_name)

    def set_devicewithl(self, enable=True, version=1):
        return self.__dobotlink.Magician.SetDeviceWithL(
            portName=self.__port_name, enable=enable, version=version)

    def get_devicewithl(self):
        return self.__dobotlink.Magician.GetDeviceWithL(
            portName=self.__port_name)

    def get_devicetime(self):
        return self.__dobotlink.Magician.GetDeviceTime(
            portName=self.__port_name)

    def get_deviceid(self):
        return self.__dobotlink.Magician.GetDeviceID(portName=self.__port_name)

    def get_productname(self):
        return self.__dobotlink.Magician.GetProductName(
            portName=self.__port_name)

    def queuedcmd_start(self):
        return self.__dobotlink.Magician.QueuedCmdStart(
            portName=self.__port_name)

    def queuedcmd_stop(self, force_stop=False):
        return self.__dobotlink.Magician.QueuedCmdStop(
            portName=self.__port_name, forceStop=force_stop)

    def queuedcmd_clear(self):
        return self.__dobotlink.Magician.QueuedCmdClear(
            portName=self.__port_name)

    def queuedcmd_startdownload(self, total_loop, lineper_loop):
        return self.__dobotlink.Magician.QueuedCmdStartDownload(
            portName=self.__port_name,
            totalLoop=total_loop,
            linePerLoop=lineper_loop)

    def queuedcmd_stopdownload(self):
        return self.__dobotlink.Magician.QueuedCmdStopDownload(
            portName=self.__port_name)

    def get_queuedcmd_currentindex(self):
        return self.__dobotlink.Magician.GetQueuedCmdCurrentIndex(
            portName=self.__port_name)

    def get_queuedcmd_leftspace(self):
        return self.__dobotlink.Magician.GetQueuedCmdLeftSpace(
            portName=self.__port_name)

    def set_armspeed_ratio(self,
                           set_type: int,
                           set_value: int,
                           is_queued=False):
        return self.__dobotlink.Magician.SetArmSpeedRatio(
            portName=self.__port_name,
            type=set_type,
            value=set_value,
            isQueued=is_queued)

    def get_armspeed_ratio(self, get_type: int):
        return self.__dobotlink.Magician.GetArmSpeedRatio(
            portName=self.__port_name, type=get_type)

    def set_servoangle(self, index: int, set_value: float, is_queued=False):
        return self.__dobotlink.Magician.SetServoAngle(
            portName=self.__port_name,
            index=index,
            value=set_value,
            isQueued=is_queued)

    def get_servoangle(self, index: int):
        return self.__dobotlink.Magician.GetServoAngle(
            portName=self.__port_name, index=index)

    def set_lspeed_ratio(self, set_type: int, set_value: int, is_queued=False):
        return self.__dobotlink.Magician.SetLSpeedRatio(
            portName=self.__port_name,
            type=set_type,
            value=set_value,
            isQueued=is_queued)

    def get_lspeed_ratio(self, get_type: int):
        return self.__dobotlink.Magician.GetLSpeedRatio(
            portName=self.__port_name, type=get_type)

    def get_pose(self):
        return self.__dobotlink.Magician.GetPose(portName=self.__port_name)

    def reset_pose(self,
                   manual_enable,
                   rear_armangle=None,
                   front_armangle=None):
        return self.__dobotlink.Magician.ResetPose(
            portName=self.__port_name,
            manualEnable=manual_enable,
            rearArmAngle=rear_armangle,
            frontArmAngle=front_armangle)

    def get_posel(self):
        return self.__dobotlink.Magician.GetPoseL(portName=self.__port_name)

    def get_alarms_state(self):
        return self.__dobotlink.Magician.GetAlarmsState(
            portName=self.__port_name)

    def clear_allalarms_state(self):
        return self.__dobotlink.Magician.ClearAllAlarmsState(
            portName=self.__port_name)

    def set_homeparams(self,
                       x: float,
                       y: float,
                       z: float,
                       r: float,
                       is_queued=False):
        return self.__dobotlink.Magician.SetHOMEParams(
            portName=self.__port_name, x=x, y=y, z=z, r=r, isQueued=is_queued)

    def get_homeparams(self):
        return self.__dobotlink.Magician.GetHOMEParams(
            portName=self.__port_name)

    def set_homecmd(self,
                    is_queued=True,
                    iswait_forfinish=True,
                    time_out=25000):
        return self.__dobotlink.Magician.SetHOMECmd(
            portName=self.__port_name,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    def set_autoleveling(self,
                         enable: bool,
                         precision: float,
                         is_queued=False):
        return self.__dobotlink.Magician.SetAutoLeveling(
            portName=self.__port_name,
            enable=enable,
            precision=precision,
            isQueued=is_queued)

    def get_autoleveling(self):
        return self.__dobotlink.Magician.GetAutoLeveling(
            portName=self.__port_name)

    def set_hhttrig_mode(self, mode: int, is_queued=False):
        return self.__dobotlink.Magician.SetHHTTrigMode(
            portName=self.__port_name, mode=mode, isQueued=is_queued)

    def get_hhttrig_mode(self):
        return self.__dobotlink.Magician.GetHHTTrigMode(
            portName=self.__port_name)

    def set_hhttrig_output_enabled(self, enable: bool, is_queued=False):
        return self.__dobotlink.Magician.SetHHTTrigOutputEnabled(
            portName=self.__port_name, enable=enable, isQueued=is_queued)

    def get_hhttrig_output_enabled(self):
        return self.__dobotlink.Magician.GetHHTTrigOutputEnabled(
            portName=self.__port_name)

    def get_hhttrig_output(self):
        return self.__dobotlink.Magician.GetHHTTrigOutput(
            portName=self.__port_name)

    def set_endeffector_params(self,
                               x_offset: float,
                               y_offset: float,
                               z_offset: float,
                               is_queued=False):
        return self.__dobotlink.Magician.SetEndEffectorParams(
            portName=self.__port_name,
            xOffset=x_offset,
            yOffset=y_offset,
            zOffset=z_offset,
            isQueued=is_queued)

    def get_endeffector_params(self):
        return self.__dobotlink.Magician.GetEndEffectorParams(
            portName=self.__port_name)

    def set_endeffector_type(self, set_type: int, is_queued=False):
        return self.__dobotlink.Magician.SetEndEffectorType(
            portName=self.__port_name, type=set_type, isQueued=is_queued)

    def get_endeffector_type(self):
        return self.__dobotlink.Magician.GetEndEffectorType(
            portName=self.__port_name)

    def set_endeffector_laser(self, enable: bool, on: bool, is_queued=False):
        return self.__dobotlink.Magician.SetEndEffectorLaser(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_laser(self):
        return self.__dobotlink.Magician.GetEndEffectorLaser(
            portName=self.__port_name)

    def set_endeffector_suctioncup(self,
                                   enable: bool,
                                   on: bool,
                                   is_queued=False):
        return self.__dobotlink.Magician.SetEndEffectorSuctionCup(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_suctioncup(self):
        return self.__dobotlink.Magician.GetEndEffectorSuctionCup(
            portName=self.__port_name)

    def set_endeffector_gripper(self, enable: bool, on: bool, is_queued=False):
        return self.__dobotlink.Magician.SetEndEffectorGripper(
            portName=self.__port_name,
            enable=enable,
            on=on,
            isQueued=is_queued)

    def get_endeffector_gripper(self):
        return self.__dobotlink.Magician.GetEndEffectorGripper(
            portName=self.__port_name)

    def set_jogjoint_params(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.Magician.SetJOGJointParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_jogjoint_params(self):
        return self.__dobotlink.Magician.GetJOGJointParams(
            portName=self.__port_name)

    def set_jogcoordinate_params(self,
                                 velocity,
                                 acceleration,
                                 is_queued=False):
        return self.__dobotlink.Magician.SetJOGCoordinateParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_jogcoordinate_params(self):
        return self.__dobotlink.Magician.GetJOGCoordinateParams(
            portName=self.__port_name)

    def set_jogcommon_params(self,
                             velocity_ratio,
                             acceleration_ratio,
                             is_queued=False):
        return self.__dobotlink.Magician.SetJOGCommonParams(
            portName=self.__port_name,
            velocityRatio=velocity_ratio,
            accelerationRatio=acceleration_ratio,
            isQueued=is_queued)

    def get_jogcommon_params(self):
        return self.__dobotlink.Magician.GetJOGCommonParams(
            portName=self.__port_name)

    def set_jogl_params(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.Magician.SetJOGLParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_jogl_params(self):
        return self.__dobotlink.Magician.GetJOGLParams(
            portName=self.__port_name)

    def set_jogcmd(self, is_joint, cmd, is_queued):
        return self.__dobotlink.Magician.SetJOGCmd(portName=self.__port_name,
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
        return self.__dobotlink.Magician.SetPTPCmd(
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
        return self.__dobotlink.Magician.SetRCmd(
            portName=self.__port_name,
            r=r,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    def set_ptpwithl_cmd(self,
                         ptp_mode: int,
                         x: float,
                         y: float,
                         z: float,
                         r: float,
                         l: float,
                         is_queued=True,
                         iswait_forfinish=True):
        return self.__dobotlink.Magician.SetPTPWithLCmd(
            portName=self.__port_name,
            ptpMode=ptp_mode,
            x=x,
            y=y,
            z=z,
            r=r,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish)

    def set_ptpjoint_param(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.Magician.SetPTPJointParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_ptpjoint_param(self):
        return self.__dobotlink.Magician.GetPTPJointParams(
            portName=self.__port_name)

    def set_ptpcoordinate_params(self,
                                 xyz_velocity,
                                 r_velocity,
                                 xyz_acceleration,
                                 r_acceleration,
                                 is_queued=False):
        return self.__dobotlink.Magician.SetPTPCoordinateParams(
            portName=self.__port_name,
            xyzVelocity=xyz_velocity,
            rVelocity=r_velocity,
            xyzAcceleration=xyz_acceleration,
            rAcceleration=r_acceleration,
            isQueued=is_queued)

    def get_ptpcoordinate_params(self):
        return self.__dobotlink.Magician.GetPTPCoordinateParams(
            portName=self.__port_name)

    def set_ptpjump_params(self, z_limit, jump_height, is_queued=False):
        return self.__dobotlink.Magician.SetPTPJumpParams(
            portName=self.__port_name,
            zLimit=z_limit,
            jumpHeight=jump_height,
            isQueued=is_queued)

    def get_ptpjump_params(self):
        return self.__dobotlink.Magician.GetPTPJumpParams(
            portName=self.__port_name)

    def set_ptpcommon_params(self,
                             velocity_ratio,
                             acceleration_ratio,
                             is_queued=False):
        return self.__dobotlink.Magician.SetPTPCommonParams(
            portName=self.__port_name,
            velocityRatio=velocity_ratio,
            accelerationRatio=acceleration_ratio,
            isQueued=is_queued)

    def get_ptpcommon_params(self):
        return self.__dobotlink.Magician.GetPTPCommonParams(
            portName=self.__port_name)

    def set_ptpl_params(self, velocity, acceleration, is_queued=False):
        return self.__dobotlink.Magician.SetPTPLParams(
            portName=self.__port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    def get_ptpl_params(self):
        return self.__dobotlink.Magician.GetPTPLParams(
            portName=self.__port_name)

    def set_ptpjump2_params(self,
                            z_limit,
                            start_jump_height,
                            end_jump_height,
                            is_queued=False):
        return self.__dobotlink.Magician.SetPTPJump2Params(
            portName=self.__port_name,
            zLimit=z_limit,
            startJumpHeight=start_jump_height,
            endJumpHeight=end_jump_height,
            isQueued=is_queued)

    def get_ptpjump2_params(self):
        return self.__dobotlink.Magician.GetPTPJump2Params(
            portName=self.__port_name)

    def set_iomultiplexing(self, port: int, multiplex: int, is_queued=False):
        return self.__dobotlink.Magician.SetIOMultiplexing(
            portName=self.__port_name,
            port=port,
            multiplex=multiplex,
            isQueued=is_queued)

    def get_iomultiplexing(self, port: int):
        return self.__dobotlink.Magician.GetIOMultiplexing(
            portName=self.__port_name, port=port)

    def set_iodo(self, port, level, is_queued=False):
        return self.__dobotlink.Magician.SetIODO(portName=self.__port_name,
                                                 port=port,
                                                 level=level,
                                                 isQueued=is_queued)

    def get_iodo(self, port):
        return self.__dobotlink.Magician.GetIODO(portName=self.__port_name,
                                                 port=port)

    def set_iopwm(self, port, frequency, duty_cycle, is_queued=False):
        return self.__dobotlink.Magician.SetIOPWM(portName=self.__port_name,
                                                  port=port,
                                                  frequency=frequency,
                                                  dutyCycle=duty_cycle,
                                                  isQueued=is_queued)

    def get_iopwm(self, port):
        return self.__dobotlink.Magician.GetIOPWM(portName=self.__port_name,
                                                  port=port)

    def get_iodi(self, port):
        return self.__dobotlink.Magician.GetIODI(portName=self.__port_name,
                                                 port=port)

    def get_ioadc(self, port):
        return self.__dobotlink.Magician.GetIOADC(portName=self.__port_name,
                                                  port=port)

    def set_emotor(self, index, enable, speed, is_queued=False):
        return self.__dobotlink.Magician.SetEMotor(portName=self.__port_name,
                                                   index=index,
                                                   enable=enable,
                                                   speed=speed,
                                                   isQueued=is_queued)

    def set_emotors(self, index, enable, speed, distance, is_queued=False):
        return self.__dobotlink.Magician.SetEMotorS(portName=self.__port_name,
                                                    index=index,
                                                    enable=enable,
                                                    speed=speed,
                                                    distance=distance,
                                                    isQueued=is_queued)

    def set_color_sensor(self, port, enable, version, is_queued=False):
        return self.__dobotlink.Magician.SetColorSensor(
            portName=self.__port_name,
            port=port,
            enable=enable,
            version=version,
            isQueued=is_queued)

    def get_color_sensor(self):
        return self.__dobotlink.Magician.GetColorSensor(
            portName=self.__port_name)

    def set_infrared_sensor(self, port, enable, version, is_queued=False):
        return self.__dobotlink.Magician.SetInfraredSensor(
            portName=self.__port_name,
            port=port,
            enable=enable,
            version=version,
            isQueued=is_queued)

    def get_infrared_sensor(self, port):
        return self.__dobotlink.Magician.GetInfraredSensor(
            portName=self.__port_name, port=port)

    def set_loststep_value(self, value):
        return self.__dobotlink.Magician.SetLostStepValue(
            portName=self.__port_name, value=value)

    def set_loststep_cmd(self, is_queued=False):
        return self.__dobotlink.Magician.SetLostStepCmd(
            portName=self.__port_name, isQueued=is_queued)
# 3.12 连续运动轨迹

    def set_cpparams(self,
                     target_acc,
                     junction_vel,
                     isreal_timetrack,
                     acc=None,
                     period=None,
                     is_queued=False):
        return self.__dobotlink.Magician.SetCPParams(
            portName=self.__port_name,
            targetAcc=target_acc,
            junctionVel=junction_vel,
            isRealTimeTrack=isreal_timetrack,
            acc=acc,
            period=period,
            isQueued=is_queued)

    def get_cpparams(self):
        return self.__dobotlink.Magician.GetCPParams(portName=self.__port_name)

    def set_cpcmd(self, cp_mode, x, y, z, power, is_queued=False):
        return self.__dobotlink.Magician.SetCPCmd(portName=self.__port_name,
                                                  cpMode=cp_mode,
                                                  x=x,
                                                  y=y,
                                                  z=z,
                                                  power=power,
                                                  isQueued=is_queued)

    def set_cplecmd(self, cp_mode, x, y, z, power, is_queued=False):
        return self.__dobotlink.Magician.SetCPLECmd(portName=self.__port_name,
                                                    cpMode=cp_mode,
                                                    x=x,
                                                    y=y,
                                                    z=z,
                                                    power=power,
                                                    isQueued=is_queued)


# 3.13 圆弧插补功能

    def set_arcparams(self,
                      xyz_velocity,
                      r_velocity,
                      xyz_acceleration,
                      r_acceleration,
                      is_queued=False):
        return self.__dobotlink.Magician.SetARCParams(
            portName=self.__port_name,
            xyzVelocity=xyz_velocity,
            rVelocity=r_velocity,
            xyzAcceleration=xyz_acceleration,
            rAcceleration=r_acceleration,
            isQueued=is_queued)

    def get_arcparams(self):
        return self.__dobotlink.Magician.GetARCParams(
            portName=self.__port_name)

    def set_arccmd(self, cir_point, to_point, is_queued=False):
        return self.__dobotlink.Magician.SetARCCmd(portName=self.__port_name,
                                                   cirPoint=cir_point,
                                                   toPoint=to_point,
                                                   isQueued=is_queued)

    def set_anglesensorstatic_error(self, rear_armangle_error,
                                    front_armangle_error):
        return self.__dobotlink.Magician.SetAngleSensorStaticError(
            portName=self.__port_name,
            rearArmAngleError=rear_armangle_error,
            frontArmAngleError=front_armangle_error)

    def get_anglesensorstatic_error(self):
        return self.__dobotlink.Magician.GetAngleSensorStaticError(
            portName=self.__port_name)
