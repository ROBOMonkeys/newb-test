import wpilib as wpi


class MyRobot (wpi.IterativeRobot):
    frontLeftChannel  = 0
    rearLeftChannel   = 1
    frontRightChannel  = 2
    rearRightChannel   = 3

    joystickChannel  = 0

    solenoidChannel = 0

    gyroChannel = 0

    sparkChannel = 4

    def robotInit(self):
        self.timer = wpi.Timer()

        self.deltaTime = 0

        self.drive = wpi.RobotDrive(wpi.Spark(0), wpi.Spark(1),
                                    wpi.Spark(2), wpi.Spark(3))
        self.joystick = wpi.XboxController(MyRobot.joystickChannel)
        self.solenoid = wpi.Solenoid(MyRobot.solenoidChannel)
        self.gyro = wpi.AnalogGyro(MyRobot.gyroChannel)
        self.gyro.calibrate()

        self.auto_state = 0

        self.sd = wpi.SmartDashboard()

        self.sd.putBoolean("Autonomous Center", False)
        self.sd.putBoolean("Autonomous Left", False)
        self.sd.putBoolean("Autonomous Right", False)

        #self.auto_chooser = wpi.SendableChooser()
        #self.auto_chooser.addObject("Left", 1)
        #self.auto_chooser.addObject("Center", 2)
        #self.auto_chooser.addObject("Right", 3)
        #wpi.SmartDashboard.putData("Autonomouse Position", self.auto_chooser)

        self.solenoid.set(False)
        self.sd.putString("Piston Extended", str(self.solenoid.get()))

        self.drivestate = False
        self.sd.putString("Slow mode Activated", str(self.drivestate))

    def autonomousInit(self):
        # self.auto_state = self.auto_chooser.getSelected()

        if self.sd.getBoolean("Autonomous Center"):
            self.auto_state = 2
        elif self.sd.getBoolean("Autonomous Right"):
            self.auto_state = 1
        elif self.sd.getBoolean("Autonomous Left"):
            self.auto_state = 3

        self.gyro.reset()

        self.timer.stop()
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        #One second at half speed = 8ft
        #wpi.DriverStation.reportWarning(str(self.gyro.getAngle()), False)
        if self.auto_state == 1:
        # for right side autonomous
            if self.timer.get() < 1.104:
                self.drive.mecanumDrive_Cartesian(0, 0, .75, 0)
            elif self.timer.get() < 1.67:
                self.drive.mecanumDrive_Cartesian(0, .5, 0, 0)
            elif self.timer.get() < 4:
                self.drive.mecanumDrive_Cartesian(0, 0, .25, 0)
            else:
                self.drive.mecanumDrive_Cartesian(0, 0, 0, 0)
        elif self.auto_state == 2:
        # for center autonomous
            if self.timer.get() < .6:
                self.drive.mecanumDrive_Cartesian(0, 0, .5, 0)
            elif self.timer.get() < 3.8:
                self.drive.mecanumDrive_Cartesian(0, 0, .25, 0)
            elif self.timer.get() < 8.8:
                self.drive.mecanumDrive_Cartesian(0, 0, 0, 0)
            elif self.timer.get() < 9.3:
                self.drive.mecanumDrive_Cartesian(0, 0, -.5, 0)
            else:
                self.drive.mecanumDrive_Cartesian(0, 0, 0, 0)
        elif self.auto_state == 3:
            #for left side autonomous
            if self.timer.get() < 1.104:
                self.drive.mecanumDrive_Cartesian(0, 0, .5, 0)
            elif self.timer.get() < 1.434:
                self.drive.mecanumDrive_Cartesian(0, -.5, 0, 0)
            elif self.timer.get() < 2.111:
                self.drive.mecanumDrive_Cartesian(0, 0, .25, 0)
            else:
                self.drive.mecanumDrive_Cartesian(0, 0, 0, 0)



    def teleopInit(self):
        self.timer.stop()
        self.timer.reset()
        self.timer.start()

    def teleopPeriodic(self):
        #wpi.DriverStation.reportWarning(str(self.gyro.getAngle()), False)
        lefty = -self.joystick.getY(wpi.GenericHID.Hand.kLeft)
        leftx = self.joystick.getX(wpi.GenericHID.Hand.kLeft)
        rightx = self.joystick.getX(wpi.GenericHID.Hand.kRight)

        if lefty < 0.25 and lefty > -0.25:
            lefty = 0
        if rightx < 0.25 and rightx > -0.25:
            rightx = 0
        if leftx < 0.25 and leftx > -0.25:
            leftx = 0


        #self.drive.mecanumDrive_Cartesian(-leftx/2, -rightx/2, -lefty/2)

        #self.drive.mecanumDrive_Cartesian(-leftx, -rightx, lefty, 0)
        if self.joystick.getAButton() and self.timer.get() > 0.2:
            state = self.solenoid.get()
            self.timer.reset()
            if state == False:
                self.solenoid.set(True)
            else:
                self.solenoid.set(False)
        if self.joystick.getYButton() and self.timer.get() > 0.2:
            self.timer.reset()
            if self.drivestate:
                self.drivestate = False
            else:
                self.drivestate = True


        if self.drivestate == True:
            rightx = rightx / 2
            lefty = lefty / 2
            leftx = leftx / 2

        self.sd.putString("Slow Mode Activated", str(self.drivestate))
        self.sd.putString("Piston Extended", str(self.solenoid.get()))

        self.drive.mecanumDrive_Cartesian(-leftx, -rightx, lefty, 0)





if __name__ == '__main__':
    wpi.run(MyRobot)