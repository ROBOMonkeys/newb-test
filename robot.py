import wpilib as wpi


class MyRobot (wpi.IterativeRobot):
    frontLeftChannel  = 0
    rearLeftChannel   = 1
    frontRightChannel  = 2
    rearRightChannel   = 3

    joystickChannel  = 0

    solenoidChannel = 0

    def robotInit(self):
        self.timer = wpi.Timer()

        self.deltaTime = 0
#        self.motors = [wpi.Spark(x) for x in range(4)]

        self.drive = wpi.RobotDrive(0, 1, 2, 3)#self.motors[MyRobot.frontLeftChannel],
                                    #self.motors[MyRobot.rearLeftChannel],
                                    #self.motors[MyRobot.frontRightChannel],
                                    #self.motors[MyRobot.rearRightChannel])
        self.joystick = wpi.XboxController(MyRobot.joystickChannel)
        self.solenoid = wpi.Solenoid(MyRobot.solenoidChannel)
        self.gyro = wpi.GyroBase

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        #Middle
        self.gyro.getAngle()
        self.drive.mecanumDrive_Cartesian(0, 3*.5, 0, self.gyro):


    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        lefty = self.joystick.getY(wpi.GenericHID.Hand.kLeft)
        leftx = self.joystick.getX(wpi.GenericHID.Hand.kLeft)
        rightx = self.joystick.getX(wpi.GenericHID.Hand.kRight)

        if lefty < 0.25 and lefty > -0.25:
            lefty = 0
        if rightx < 0.25 and rightx > -0.25:
            rightx = 0
        if leftx < 0.25 and leftx > -0.25:
            leftx = 0

        self.drive.mecanumDrive_Cartesian(-leftx, -rightx, -lefty, 0)
        if self.joystick.getAButton():
            state = self.solenoid.get()
            if state == True:
                self.solenoid.set(False)
            else:
                self.solenoid.set(True)


if __name__ == '__main__':
    wpi.run(MyRobot)