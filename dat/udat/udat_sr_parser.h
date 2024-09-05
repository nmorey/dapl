/*
 * Copyright (c) 2002-2005, Network Appliance, Inc. All rights reserved.
 *
 * This Software is licensed under one of the following licenses:
 *
 * 1) under the terms of the "Common Public License 1.0" a copy of which is
 *    in the file LICENSE.txt in the root directory. The license is also
 *    available from the Open Source Initiative, see
 *    http://www.opensource.org/licenses/cpl.php.
 *
 * 2) under the terms of the "The BSD License" a copy of which is in the file
 *    LICENSE2.txt in the root directory. The license is also available from
 *    the Open Source Initiative, see
 *    http://www.opensource.org/licenses/bsd-license.php.
 *
 * 3) under the terms of the "GNU General Public License (GPL) Version 2" a 
 *    copy of which is in the file LICENSE3.txt in the root directory. The 
 *    license is also available from the Open Source Initiative, see
 *    http://www.opensource.org/licenses/gpl-license.php.
 *
 * Licensee has the right to choose one of the above licenses.
 *
 * Redistributions of source code must retain the above copyright
 * notice and one of the license notices.
 *
 * Redistributions in binary form must reproduce both the above copyright
 * notice, one of the license notices in the documentation
 * and/or other materials provided with the distribution.
 */

/**********************************************************************
 * 
 * HEADER: dat_sr_parser.h
 *
 * PURPOSE: static registry (SR) parser inteface declarations
 *
 * $Id: udat_sr_parser.h,v 1.4 2005/03/24 05:58:36 jlentini Exp $
 **********************************************************************/

#ifndef _DAT_SR_PARSER_H_
#define _DAT_SR_PARSER_H_


#include "dat_osd.h"


/*********************************************************************
 *                                                                   *
 * Function Declarations                                             *
 *                                                                   *
 *********************************************************************/

/*
 * The static registry exports the same interface regardless of 
 * platform. The particular implementation of dat_sr_load() is 
 * found with other platform dependent sources.
 */

extern DAT_RETURN 
dat_sr_load (void);


#endif /* _DAT_SR_PARSER_H_ */
